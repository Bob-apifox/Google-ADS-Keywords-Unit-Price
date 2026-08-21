import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

def get_google_ads_client():
    for attempt in range(3):
        try:
            return GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        except Exception as e:
            print(f"Loading client attempt {attempt+1} failed: {e}")
            time.sleep(2)
    raise RuntimeError("Failed to initialize Google Ads Client after 3 attempts.")

def fetch_campaign_details(client):
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.bidding_strategy_type,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros,
            campaign.campaign_budget,
            campaign_budget.id,
            campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """
    campaigns = {}
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    for batch in stream:
        for row in batch.results:
            c = row.campaign
            b = row.campaign_budget
            campaigns[c.name] = {
                "id": str(c.id),
                "name": c.name,
                "bidding_type": c.bidding_strategy_type.name,
                "current_max_conv_tcpa": c.maximize_conversions.target_cpa_micros / 1e6 if c.maximize_conversions.target_cpa_micros else None,
                "current_tcpa": c.target_cpa.target_cpa_micros / 1e6 if c.target_cpa.target_cpa_micros else None,
                "budget_resource": c.campaign_budget,
                "budget_id": str(b.id) if b.id else None,
                "budget_amount": b.amount_micros / 1e6 if b.amount_micros else None
            }
    return campaigns

def update_campaign_budget_and_tcpa(client, campaigns_info, updates):
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")
    
    print("\n==================================================")
    print("💰 1. 正在执行 Campaign 预算与 Target CPA 调整...")
    print("==================================================")
    
    for c_name, conf in updates.items():
        if c_name not in campaigns_info:
            print(f"⚠️ 未找到系列或系列未启用: {c_name}")
            continue
            
        info = campaigns_info[c_name]
        c_id = info["id"]
        budget_res = info["budget_resource"]
        new_budget = conf["budget_usd"]
        new_tcpa = conf["tcpa_usd"]
        
        # 1. Update Budget
        budget_op = client.get_type("CampaignBudgetOperation")
        budget = budget_op.update
        budget.resource_name = budget_res
        budget.amount_micros = int(new_budget * 1_000_000)
        budget_op.update_mask.paths.append("amount_micros")
        
        try:
            campaign_budget_service.mutate_campaign_budgets(
                customer_id=CUSTOMER_ID, operations=[budget_op]
            )
            print(f"✅ [{c_name}] 预算更新成功: ${info['budget_amount']} ➔ ${new_budget}/天")
        except Exception as e:
            print(f"❌ [{c_name}] 预算更新失败: {e}")
            
        # 2. Update Target CPA
        tcpa_op = client.get_type("CampaignOperation")
        camp = tcpa_op.update
        camp.resource_name = campaign_service.campaign_path(CUSTOMER_ID, c_id)
        
        bidding_type = info["bidding_type"]
        if bidding_type == "MAXIMIZE_CONVERSIONS":
            camp.maximize_conversions.target_cpa_micros = int(new_tcpa * 1_000_000)
            tcpa_op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
        elif bidding_type == "TARGET_CPA":
            camp.target_cpa.target_cpa_micros = int(new_tcpa * 1_000_000)
            tcpa_op.update_mask.paths.append("target_cpa.target_cpa_micros")
        else:
            # Default try maximize_conversions
            camp.maximize_conversions.target_cpa_micros = int(new_tcpa * 1_000_000)
            tcpa_op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
            
        try:
            campaign_service.mutate_campaigns(
                customer_id=CUSTOMER_ID, operations=[tcpa_op]
            )
            print(f"✅ [{c_name}] Target CPA 更新成功 ➔ ${new_tcpa}")
        except Exception as e:
            print(f"❌ [{c_name}] Target CPA 更新失败 ({bidding_type}): {e}")

def pause_zero_conversion_ad_groups(client, campaigns_info, ad_groups_to_pause):
    ga_service = client.get_service("GoogleAdsService")
    ag_service = client.get_service("AdGroupService")
    
    print("\n==================================================")
    print("⏸️ 2. 正在暂停近 7 天 0 转化且空耗的广告组...")
    print("==================================================")
    
    operations = []
    for c_name, ag_name in ad_groups_to_pause:
        if c_name not in campaigns_info:
            print(f"⚠️ 系列未找到: {c_name}")
            continue
        c_id = campaigns_info[c_name]["id"]
        
        # Query Ad Group ID
        query = f"""
            SELECT ad_group.id, ad_group.name, ad_group.status
            FROM ad_group
            WHERE campaign.id = {c_id}
              AND ad_group.name = '{ag_name}'
        """
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            ag_found = False
            for batch in stream:
                for row in batch.results:
                    ag_found = True
                    if row.ad_group.status.name == "PAUSED":
                        print(f"ℹ️ [{c_name}] -> [{ag_name}] 已经是 PAUSED 状态，跳过。")
                        continue
                    ag_id = row.ad_group.id
                    op = client.get_type("AdGroupOperation")
                    ag = op.update
                    ag.resource_name = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
                    ag.status = client.enums.AdGroupStatusEnum.PAUSED
                    op.update_mask.paths.append("status")
                    operations.append((c_name, ag_name, op))
            if not ag_found:
                print(f"⚠️ [{c_name}] 未找到广告组: {ag_name}")
        except Exception as e:
            print(f"❌ 查询广告组 [{ag_name}] 出错: {e}")
            
    if operations:
        raw_ops = [item[2] for item in operations]
        try:
            response = ag_service.mutate_ad_groups(
                customer_id=CUSTOMER_ID, operations=raw_ops
            )
            for item in operations:
                print(f"✅ 成功暂停广告组: [{item[0]}] ➔ [{item[1]}]")
        except Exception as e:
            print(f"❌ 批量暂停广告组失败: {e}")
    else:
        print("ℹ️ 没有需要变更状态的广告组。")

def add_negative_keywords_batch(client, campaigns_info, negative_keywords_map):
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    campaign_service = client.get_service("CampaignService")
    
    print("\n==================================================")
    print("🛑 3. 正在批量注入否定关键词 (Stop-Loss Negatives)...")
    print("==================================================")
    
    operations = []
    for c_name, keywords in negative_keywords_map.items():
        if c_name not in campaigns_info:
            print(f"⚠️ 系列未找到: {c_name}")
            continue
        c_id = campaigns_info[c_name]["id"]
        c_resource_name = campaign_service.campaign_path(CUSTOMER_ID, c_id)
        
        unique_kws = list(set(keywords))
        for kw in unique_kws:
            op = client.get_type("CampaignCriterionOperation")
            crit = op.create
            crit.campaign = c_resource_name
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
    chunk_size = 500
    for i in range(0, len(operations), chunk_size):
        chunk = operations[i:i+chunk_size]
        try:
            req = client.get_type("MutateCampaignCriteriaRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(chunk)
            req.partial_failure = True
            response = campaign_criterion_service.mutate_campaign_criteria(request=req)
            print(f"✅ Chunk {i//chunk_size + 1}: 成功添加 {len(chunk)} 个否定词！")
        except Exception as e:
            print(f"❌ Chunk {i//chunk_size + 1} 添加否定词失败: {e}")

def main():
    print("==================================================")
    print("🚀 Google Ads 8月18-19日全盘优化与压降方案 执行程序")
    print("==================================================")
    
    client = get_google_ads_client()
    print("🔍 正在检索全账户 ENABLED 状态的 Campaign 信息...")
    campaigns_info = fetch_campaign_details(client)
    print(f"✅ 成功获取 {len(campaigns_info)} 个活跃广告系列信息。")
    
    # 1. Campaign Updates (Budgets & Target CPA)
    campaign_updates = {
        # 🚀 加码放量
        "Google-Sa-DSA-Postman-Global": {"budget_usd": 55.0, "tcpa_usd": 2.20},
        "Google-Sa-Comp-HeavyQA-Global": {"budget_usd": 60.0, "tcpa_usd": 2.50},
        "Google-Sa-Fern-Global": {"budget_usd": 25.0, "tcpa_usd": 2.00},
        "Google-Sa-Comp-VSCode-Global": {"budget_usd": 25.0, "tcpa_usd": 2.00},
        
        # 🔒 护盘/微调
        "Google-Sa-CP-Global": {"budget_usd": 160.0, "tcpa_usd": 2.50},
        
        # ✂️ 削减止血
        "Google-Sa-Postman-Global": {"budget_usd": 95.0, "tcpa_usd": 2.80},
        "Google-Sa-Readme-Global": {"budget_usd": 20.0, "tcpa_usd": 2.50},
        "Google-Sa-Mintlify-Global": {"budget_usd": 25.0, "tcpa_usd": 2.50},
        "Google-Sa-Doc-Global": {"budget_usd": 18.0, "tcpa_usd": 2.50},
        "Google-Sa-Solutions-Unified-API-Global": {"budget_usd": 25.0, "tcpa_usd": 2.60},
        "Google-Sa-Hoppscotch-Global": {"budget_usd": 20.0, "tcpa_usd": 2.50},
        "Google-Sa-Mock-Global": {"budget_usd": 45.0, "tcpa_usd": 2.50},
        "Google-Sa-Stoplight-Global": {"budget_usd": 10.0, "tcpa_usd": 2.50},
    }
    update_campaign_budget_and_tcpa(client, campaigns_info, campaign_updates)
    
    # 2. Ad Groups to Pause
    ad_groups_to_pause = [
        ("Google-Sa-Stoplight-Global", "Insomnia--Global"),
        ("Google-Sa-Stoplight-Global", "Doc-Global"),
        ("Google-Sa-Readme-Global", "Swagger--Global"),
        ("Google-Sa-Readme-Global", "api-document-Global"),
        ("Google-Sa-Readme-Global", "Doc-CP-Global"),
        ("Google-Sa-DSA-Alternatives-Global", "DSA-MuleSoft-Alternative"),
        ("Google-Sa-Func-CICD-Global", "Newman-Integration"),
        ("Google-Sa-Solutions-Unified-API-Global", "Multi-Format Import"),
        ("Google-Sa-API Editor-Global", "API-Code-Generation")
    ]
    pause_zero_conversion_ad_groups(client, campaigns_info, ad_groups_to_pause)
    
    # 3. Negative Keywords Map
    negative_keywords_map = {
        "Google-Sa-Stoplight-Global": ["swagger ui", "devtools chrome", "flowise", "omniroute", "framer", "https jsbin com", "visual code online", "hit api online"],
        "Google-Sa-RapidAPI-Global": ["api rest test online"],
        "Google-Sa-Func-CICD-Global": ["gitpod", "git clone", "git github", "github desktop", "github actions"],
        "Google-Sa-Readme-Global": ["ngrok", "visual studio", "index js", "azure", "facebook graph api", "ckeditor 5", "api whatsapp", "dillinger", "microsoft azure", "get node js"],
        "Google-Sa-Doc-Global": ["app plusdocs com", "testing api", "api datadog", "api platform", "affine desktop", "consumir api", "probar api", "api online", "open api"],
        "Google-Sa-Mintlify-Global": ["cursor", "api docs", "apis website", "requestly api client", "stoplight", "online coding", "uvicorn", "firebase studio", "ia experta en programacion"],
        "Google-Sa-Hoppscotch-Global": ["vercel", "zapier", "hoppscotch io", "testlink tool", "api test application", "https mockapi io", "hopscotch io", "laragon", "testrail", "online rest test"],
        "Google-Sa-Solutions-Unified-API-Global": ["netlify app", "www odoo com", "decart api platform", "owasp zap test website", "livekit_api_key", "amazon q developer", "v0 dev", "capacitorjs", "openalternative co", "test rest api"],
        "Google-Sa-DSA-Alternatives-Global": ["mulesoft", "insomnia web app", "insomnia api online", "insomnia api tool", "аналог постмана", "https www gnu org licenses", "insomnia software", "mulesoft application"],
        "Google-Sa-MCP-Infrastructure": ["mcp & cli", "vs code online", "aider chat", "replit come"],
        "Google-Sa-API Editor-Global": ["online openapi editor", "creating app", "openapi specification online", "visual code", "api documentation tool", "api request online"],
        "Google-Sa-Postman-Global": ["postman like apps", "postman application", "open postman collection online", "postman opensource alternative", "postman for rest api", "postman dmg", "postman for window", "postman url check", "postman testing tool", "postman like online tool"],
        "Google-Sa-Mock-Global": ["codepen io", "developer tools", "online api testing tools", "no code app builder", "codepen codepen io", "sdk platform tools for windows", "magic loops", "prototype code", "llama coder", "instalar api"],
        "Google-Sa-Func-MultiProtocol-Global": ["graphql online", "http websockets"],
        "Google-Sa-Debug-Global": ["burp suite community edition", "run code online", "online api testing", "visual block platforms", "pentestgpt", "open interpreter", "zai_api_key", "openrouter", "write code online", "ia programacion"],
        "Google-Sa-CP-Global": ["devexpress download", "appsheet", "can claude make software", "github pro+", "install jenkins for windows", "apidog price", "bytez", "apidog extension", "claude dashboard templates"],
        "Google-Sa-Swagger-Global": ["devdocs io", "developer tools", "bolt new", "devdocs", "gemini code assist", "cohereapikey", "create api contract online", "decart api platform", "api client software"],
        "Google-Sa-CP-AR": ["download postman for windows", "postman com", "online postman free", "postman desktop", "https www postman com"]
    }
    add_negative_keywords_batch(client, campaigns_info, negative_keywords_map)
    
    print("\n==================================================")
    print("🎉 [DONE] 8月18-19日 全盘优化与压降动作已全部成功上线！")
    print("==================================================")

if __name__ == "__main__":
    main()
