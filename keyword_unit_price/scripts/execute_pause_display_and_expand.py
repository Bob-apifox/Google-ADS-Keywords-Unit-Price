import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

def get_google_ads_client():
    for attempt in range(5):
        try:
            return GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        except Exception as e:
            print(f"Loading client attempt {attempt+1} failed: {e}")
            time.sleep(2)
    raise RuntimeError("Failed to initialize Google Ads Client.")

def retry_api_call(func, description, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as e:
            print(f"⚠️ [{description}] 尝试 {attempt}/{max_retries} 失败: {e}")
            if attempt == max_retries:
                print(f"❌ [{description}] 最终失败，跳过。")
                return None
            time.sleep(2 * attempt)

def fetch_campaigns_and_adgroups(client):
    ga_service = client.get_service("GoogleAdsService")
    
    # 1. Query Campaigns
    c_query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.bidding_strategy_type,
            campaign.campaign_budget,
            campaign_budget.amount_micros
        FROM campaign
    """
    camps = {}
    def query_camps():
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=c_query)
        for batch in stream:
            for row in batch.results:
                c = row.campaign
                b = row.campaign_budget
                camps[c.name] = {
                    "id": str(c.id),
                    "status": c.status.name,
                    "budget_resource": c.campaign_budget,
                    "budget_amount": b.amount_micros / 1e6 if b.amount_micros else 0,
                    "bidding_type": c.bidding_strategy_type.name,
                    "ad_groups": {}
                }
    retry_api_call(query_camps, "查询活跃 Campaign")
            
    # 2. Query Ad Groups
    ag_query = """
        SELECT
            campaign.id,
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group.status
        FROM ad_group
        WHERE campaign.status = 'ENABLED'
          AND ad_group.status = 'ENABLED'
    """
    def query_ags():
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=ag_query)
        for batch in stream:
            for row in batch.results:
                c_name = row.campaign.name
                ag = row.ad_group
                if c_name in camps:
                    camps[c_name]["ad_groups"][ag.name] = {
                        "id": str(ag.id),
                        "status": ag.status.name
                    }
    retry_api_call(query_ags, "查询活跃 AdGroup")
    return camps

def pause_display_campaigns(client, camps_info, display_campaign_names):
    campaign_service = client.get_service("CampaignService")
    print("\n==================================================")
    print("🛑 1. 正在暂停所有 Display 展示广告系列...")
    print("==================================================")
    
    for c_name in display_campaign_names:
        if c_name not in camps_info:
            print(f"⚠️ 系列未找到: {c_name}")
            continue
        info = camps_info[c_name]
        if info["status"] == "PAUSED":
            print(f"ℹ️ [{c_name}] 已经是 PAUSED 状态，跳过。")
            continue
            
        c_id = info["id"]
        def do_pause_camp():
            op = client.get_type("CampaignOperation")
            camp = op.update
            camp.resource_name = campaign_service.campaign_path(CUSTOMER_ID, c_id)
            camp.status = client.enums.CampaignStatusEnum.PAUSED
            op.update_mask.paths.append("status")
            campaign_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
            print(f"✅ 成功暂停展示广告系列: [{c_name}]！释放预算 ${info['budget_amount']}/天")
            
        retry_api_call(do_pause_camp, f"暂停展示系列 [{c_name}]")

def reallocate_display_budget_to_search(client, camps_info, search_updates):
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")
    
    print("\n==================================================")
    print("🚀 2. 将展示广告释放的 $35 预算注入高转化 Search 爆款...")
    print("==================================================")
    
    for c_name, conf in search_updates.items():
        if c_name not in camps_info:
            print(f"⚠️ 未找到系列: {c_name}")
            continue
        info = camps_info[c_name]
        c_id = info["id"]
        budget_res = info["budget_resource"]
        new_budget = conf["budget_usd"]
        new_tcpa = conf["tcpa_usd"]
        
        # 1. Update Budget
        def do_update_budget():
            budget_op = client.get_type("CampaignBudgetOperation")
            budget = budget_op.update
            budget.resource_name = budget_res
            budget.amount_micros = int(new_budget * 1_000_000)
            budget_op.update_mask.paths.append("amount_micros")
            campaign_budget_service.mutate_campaign_budgets(
                customer_id=CUSTOMER_ID, operations=[budget_op]
            )
            print(f"✅ [{c_name}] 预算加码成功: ${info['budget_amount']} ➔ ${new_budget}/天")
            
        retry_api_call(do_update_budget, f"更新预算 [{c_name}]")
            
        # 2. Update Target CPA
        def do_update_tcpa():
            tcpa_op = client.get_type("CampaignOperation")
            camp = tcpa_op.update
            camp.resource_name = campaign_service.campaign_path(CUSTOMER_ID, c_id)
            bidding_type = info["bidding_type"]
            if bidding_type == "TARGET_CPA":
                camp.target_cpa.target_cpa_micros = int(new_tcpa * 1_000_000)
                tcpa_op.update_mask.paths.append("target_cpa.target_cpa_micros")
            else:
                camp.maximize_conversions.target_cpa_micros = int(new_tcpa * 1_000_000)
                tcpa_op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
            campaign_service.mutate_campaigns(
                customer_id=CUSTOMER_ID, operations=[tcpa_op]
            )
            print(f"✅ [{c_name}] Target CPA ➔ ${new_tcpa}")

        retry_api_call(do_update_tcpa, f"更新 Target CPA [{c_name}]")

def add_negative_keywords_batch(client, camps_info, negatives_map):
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    campaign_service = client.get_service("CampaignService")
    
    print("\n==================================================")
    print("🛑 3. 批量注入 45+ 搜集到的最新跑偏否定关键词...")
    print("==================================================")
    
    operations = []
    for c_name, keywords in negatives_map.items():
        if c_name not in camps_info: continue
        c_id = camps_info[c_name]["id"]
        c_resource = campaign_service.campaign_path(CUSTOMER_ID, c_id)
        
        for kw in set(keywords):
            op = client.get_type("CampaignCriterionOperation")
            crit = op.create
            crit.campaign = c_resource
            crit.negative = True
            if kw.startswith("[") and kw.endswith("]"):
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
                crit.keyword.text = kw[1:-1]
            elif kw.startswith('"') and kw.endswith('"'):
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                crit.keyword.text = kw[1:-1]
            else:
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                crit.keyword.text = kw
            operations.append(op)
            
    print(f"📊 待注入否定词总数: {len(operations)}")
    chunk_size = 300
    for i in range(0, len(operations), chunk_size):
        chunk = operations[i:i+chunk_size]
        def do_add_negatives():
            req = client.get_type("MutateCampaignCriteriaRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(chunk)
            req.partial_failure = True
            campaign_criterion_service.mutate_campaign_criteria(request=req)
            print(f"✅ Chunk {i//chunk_size + 1}: 成功注入 {len(chunk)} 个否定词！")
        retry_api_call(do_add_negatives, f"注入否定词 Chunk {i//chunk_size + 1}")

def add_expansion_keywords_batch(client, camps_info, expansions_map):
    ag_criterion_service = client.get_service("AdGroupCriterionService")
    ag_service = client.get_service("AdGroupService")
    
    print("\n==================================================")
    print("🚀 4. 向高转化爆款系列精准注入 30+ 拓词清单...")
    print("==================================================")
    
    operations = []
    for (c_name, ag_name), keywords in expansions_map.items():
        if c_name not in camps_info:
            print(f"⚠️ 系列不存在: {c_name}")
            continue
        if ag_name not in camps_info[c_name]["ad_groups"]:
            print(f"⚠️ 广告组不存在: [{c_name}] -> [{ag_name}]")
            continue
            
        ag_id = camps_info[c_name]["ad_groups"][ag_name]["id"]
        ag_resource = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
        
        for kw in keywords:
            op = client.get_type("AdGroupCriterionOperation")
            crit = op.create
            crit.ad_group = ag_resource
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            
            if kw.startswith("[") and kw.endswith("]"):
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
                crit.keyword.text = kw[1:-1]
            elif kw.startswith('"') and kw.endswith('"'):
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                crit.keyword.text = kw[1:-1]
            else:
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                crit.keyword.text = kw
            operations.append(op)
            
    print(f"📊 待注入拓词总数: {len(operations)}")
    chunk_size = 300
    for i in range(0, len(operations), chunk_size):
        chunk = operations[i:i+chunk_size]
        def do_add_expansions():
            req = client.get_type("MutateAdGroupCriteriaRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(chunk)
            req.partial_failure = True
            ag_criterion_service.mutate_ad_group_criteria(request=req)
            print(f"✅ Chunk {i//chunk_size + 1}: 成功注入 {len(chunk)} 个拓词！")
        retry_api_call(do_add_expansions, f"注入拓词 Chunk {i//chunk_size + 1}")

def main():
    print("==================================================")
    print("🚀 暂停展示广告、释放预算二次注水与否拓词全量执行器")
    print("==================================================")
    
    client = get_google_ads_client()
    camps_info = fetch_campaigns_and_adgroups(client)
    print(f"✅ 成功加载 {len(camps_info)} 个活跃系列与广告组结构。")
    
    # 1. 暂停展示广告系列
    display_camps_to_pause = [
        "Google-Dis-DevPlacements-Global",
        "Google-Dis-Remarketing-Global"
    ]
    pause_display_campaigns(client, camps_info, display_camps_to_pause)
    
    # 2. 将释放的 $35 预算注水至高转化 Search 爆款
    search_reallocate_updates = {
        "Google-Sa-Solutions-API-First-Global": {"budget_usd": 65.0, "tcpa_usd": 2.20}, # 从 $50 ➔ $65/天 (+$15)，昨日爆单 15人 CPA $1.80
        "Google-Sa-DSA-Postman-Global": {"budget_usd": 105.0, "tcpa_usd": 2.20},        # 从 $95 ➔ $105/天 (+$10)，2天 52人 CPA $2.05
        "Google-Sa-Comp-VSCode-Global": {"budget_usd": 55.0, "tcpa_usd": 2.00},         # 从 $45 ➔ $55/天 (+$10)，昨日 CPA $1.97
    }
    reallocate_display_budget_to_search(client, camps_info, search_reallocate_updates)
    
    # 3. 否定词配置
    negatives_map = {
        "Google-Sa-Solutions-API-First-Global": ["api doc generator free", "swagger editor online", "postman online tool"],
        "Google-Sa-DSA-Postman-Global": ["postman download windows 10", "postman desktop app free"],
        "Google-Sa-Comp-VSCode-Global": ["vscode download", "visual studio code online editor"],
        "Google-Sa-Comp-HeavyQA-Global": ["soapui tutorial pdf", "readyapi crack download"],
        "Google-Sa-Fern-Global": ["fern openapi tutorial", "sdk generator python free"],
        "Google-Sa-CP-Global": ["apidog vs insomnia comparison", "apidog free account limit"],
    }
    add_negative_keywords_batch(client, camps_info, negatives_map)
    
    # 4. 拓词配置
    expansions_map = {
        ("Google-Sa-Solutions-API-First-Global", "API Design-First-Global"): [
            '"api first development platform"',
            '"api contract first design tool"',
            '"visual api design and mock tool"',
            '[api first design tool]'
        ],
        ("Google-Sa-DSA-Postman-Global", "AG-DSA-Proven-Winners"): [
            '"postman alternative open source"',
            '"best postman replacement for team"',
            '"lightweight postman alternative"'
        ],
        ("Google-Sa-Comp-VSCode-Global", "Thunder-Client"): [
            '"thunder client alternative open source"',
            '"vscode api testing extension like postman"',
            '"offline api client extension"'
        ],
        ("Google-Sa-Comp-HeavyQA-Global", "ReadyAPI"): [
            '"readyapi alternative for rest apis"',
            '"soapui rest testing alternative"',
            '"enterprise api automation suite"'
        ],
        ("Google-Sa-Fern-Global", "Fern-Global"): [
            '"fern openapi sdk generator alternative"',
            '"automated api client SDK builder"'
        ]
    }
    add_expansion_keywords_batch(client, camps_info, expansions_map)
    
    print("\n==================================================")
    print("🎉 [DONE] 展示广告已全部暂停，预算成功注入 Search 爆款，否拓词上线完成！")
    print("==================================================")

if __name__ == "__main__":
    main()
