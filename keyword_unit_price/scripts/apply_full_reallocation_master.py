import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

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
    for attempt in range(3):
        try:
            return GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        except Exception as e:
            print(f"Loading client attempt {attempt+1} failed: {e}")
            time.sleep(2)
    raise RuntimeError("Failed to initialize Google Ads Client after 3 attempts.")

def fetch_campaigns_and_adgroups(client):
    ga_service = client.get_service("GoogleAdsService")
    
    # 1. Query Campaigns
    c_query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.bidding_strategy_type,
            campaign.campaign_budget,
            campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """
    camps = {}
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=c_query)
    for batch in stream:
        for row in batch.results:
            c = row.campaign
            b = row.campaign_budget
            camps[c.name] = {
                "id": str(c.id),
                "budget_resource": c.campaign_budget,
                "budget_amount": b.amount_micros / 1e6 if b.amount_micros else 0,
                "bidding_type": c.bidding_strategy_type.name,
                "ad_groups": {}
            }
            
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
    return camps

def update_budgets_and_tcpa(client, camps_info, updates):
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")
    
    print("\n==================================================")
    print("💰 1. 执行全盘预算极值重配与 Target CPA 梯级调整...")
    print("==================================================")
    
    for c_name, conf in updates.items():
        if c_name not in camps_info:
            print(f"⚠️ 未找到系列: {c_name}")
            continue
        info = camps_info[c_name]
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
            print(f"✅ [{c_name}] 预算: ${info['budget_amount']} ➔ ${new_budget}/天")
        except Exception as e:
            print(f"❌ [{c_name}] 预算更新失败: {e}")
            
        # 2. Update Target CPA
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
            
        try:
            campaign_service.mutate_campaigns(
                customer_id=CUSTOMER_ID, operations=[tcpa_op]
            )
            print(f"✅ [{c_name}] Target CPA ➔ ${new_tcpa}")
        except Exception as e:
            print(f"❌ [{c_name}] Target CPA 更新失败: {e}")

def add_negative_keywords(client, camps_info, negatives_map):
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    campaign_service = client.get_service("CampaignService")
    
    print("\n==================================================")
    print("🛑 2. 批量注入 50+ 跨系列精准/词组否定关键词...")
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
    chunk_size = 500
    for i in range(0, len(operations), chunk_size):
        chunk = operations[i:i+chunk_size]
        try:
            req = client.get_type("MutateCampaignCriteriaRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(chunk)
            req.partial_failure = True
            campaign_criterion_service.mutate_campaign_criteria(request=req)
            print(f"✅ Chunk {i//chunk_size + 1}: 成功注入 {len(chunk)} 个否定词！")
        except Exception as e:
            print(f"❌ Chunk {i//chunk_size + 1} 注入失败: {e}")

def add_expansion_keywords(client, camps_info, expansions_map):
    ag_criterion_service = client.get_service("AdGroupCriterionService")
    ag_service = client.get_service("AdGroupService")
    
    print("\n==================================================")
    print("🚀 3. 向 6 大黄金印钞引擎精准注入 35+ 高转化拓词...")
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
            
    print(f"📊 待注入高转化拓词总数: {len(operations)}")
    chunk_size = 500
    for i in range(0, len(operations), chunk_size):
        chunk = operations[i:i+chunk_size]
        try:
            req = client.get_type("MutateAdGroupCriteriaRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(chunk)
            req.partial_failure = True
            ag_criterion_service.mutate_ad_group_criteria(request=req)
            print(f"✅ Chunk {i//chunk_size + 1}: 成功注入 {len(chunk)} 个高意向拓词！")
        except Exception as e:
            print(f"❌ Chunk {i//chunk_size + 1} 拓词注入失败: {e}")

def main():
    print("==================================================")
    print("🚀 Google Ads 零增预算重构、梯级CPA、否词与拓词全景执行")
    print("==================================================")
    
    client = get_google_ads_client()
    camps_info = fetch_campaigns_and_adgroups(client)
    print(f"✅ 成功加载 {len(camps_info)} 个活跃系列与广告组结构。")
    
    # 1. 预算与 Target CPA 重构配置
    reallocation_updates = {
        # 🔥 加码放量
        "Google-Sa-DSA-Postman-Global": {"budget_usd": 95.0, "tcpa_usd": 2.20},
        "Google-Sa-DSA-Global": {"budget_usd": 160.0, "tcpa_usd": 2.80},
        "Google-Sa-Comp-HeavyQA-Global": {"budget_usd": 90.0, "tcpa_usd": 2.50},
        "Google-Sa-Fern-Global": {"budget_usd": 50.0, "tcpa_usd": 2.00},
        "Google-Sa-Expansion-Horizon-2026": {"budget_usd": 85.0, "tcpa_usd": 3.00},
        "Google-Sa-Enterprise-Killer-Global": {"budget_usd": 45.0, "tcpa_usd": 2.50},
        "Google-Sa-Comp-VSCode-Global": {"budget_usd": 45.0, "tcpa_usd": 2.00},
        "Google-Sa-Design-Global": {"budget_usd": 45.0, "tcpa_usd": 2.00},
        "Google-Sa-Testing-Global": {"budget_usd": 40.0, "tcpa_usd": 2.50},
        "Google-Sa-Function-Global": {"budget_usd": 45.0, "tcpa_usd": 2.60},
        
        # 🔒 死锁/护盘
        "Google-Sa-Solutions-AI-LLM-Global": {"budget_usd": 110.0, "tcpa_usd": 2.80},
        "Google-Sa-CP-Global": {"budget_usd": 150.0, "tcpa_usd": 2.50},
        
        # ✂️ 严厉抽资
        "Google-Sa-The \"Great Migration\"-26": {"budget_usd": 10.0, "tcpa_usd": 2.50},
        "Google-Sa-DSA-Alternatives-Global": {"budget_usd": 15.0, "tcpa_usd": 2.50},
        "Google-Sa-Postman-Global": {"budget_usd": 70.0, "tcpa_usd": 2.50},
        "Google-Sa-Mock-Global": {"budget_usd": 25.0, "tcpa_usd": 2.50},
        "Google-Sa-Func-MultiProtocol-Global": {"budget_usd": 10.0, "tcpa_usd": 2.50},
        "Google-Sa-CP-AR": {"budget_usd": 20.0, "tcpa_usd": 2.50},
        "Google-Sa-Mintlify-Global": {"budget_usd": 15.0, "tcpa_usd": 2.50},
        "Google-Sa-Hoppscotch-Global": {"budget_usd": 10.0, "tcpa_usd": 2.50},
        "Google-Sa-Readme-Global": {"budget_usd": 10.0, "tcpa_usd": 2.50},
        "Google-Sa-Swagger-Global": {"budget_usd": 14.0, "tcpa_usd": 2.50},
        "Google-Sa-Doc-Global": {"budget_usd": 10.0, "tcpa_usd": 2.50},
        "Google-Sa-CP-JP": {"budget_usd": 5.0, "tcpa_usd": 2.50},
        "Google-Sa-CP-PT": {"budget_usd": 5.0, "tcpa_usd": 2.50},
        "Google-Sa-CP-KR": {"budget_usd": 5.0, "tcpa_usd": 2.50},
        "Google-Sa-CP-VN": {"budget_usd": 5.0, "tcpa_usd": 2.50},
        "Google-Sa-CP-FR": {"budget_usd": 5.0, "tcpa_usd": 2.50},
        "Google-Sa-Func-AdvancedMock-Global": {"budget_usd": 5.0, "tcpa_usd": 2.50},
        "Google-Sa-Func-ContractTest-Global": {"budget_usd": 5.0, "tcpa_usd": 2.50},
    }
    update_budgets_and_tcpa(client, camps_info, reallocation_updates)
    
    # 2. 否定词配置
    negatives_map = {
        "Google-Sa-Stoplight-Global": ["swagger ui", "devtools chrome", "flowise", "omniroute", "framer", "https jsbin com", "visual code online", "hit api online"],
        "Google-Sa-RapidAPI-Global": ["api rest test online"],
        "Google-Sa-Func-CICD-Global": ["gitpod", "git clone", "git github", "github desktop", "github actions", "powershell curl", "terminal command"],
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
    add_negative_keywords(client, camps_info, negatives_map)
    
    # 3. 拓词配置
    expansions_map = {
        ("Google-Sa-Comp-HeavyQA-Global", "ReadyAPI"): [
            '"readyapi alternative open source"',
            '"soapui alternative rest api"',
            '"enterprise api test automation tool"',
            '"smartbear readyapi alternative"',
            '[readyapi alternative]'
        ],
        ("Google-Sa-Comp-HeavyQA-Global", "Katalon-Karate"): [
            '"karate api testing alternative"',
            '"automated regression api testing tool"',
            '"pact contract testing tool"'
        ],
        ("Google-Sa-Fern-Global", "Fern-Global"): [
            '"fern api alternative"',
            '"fern sdk generator alternative"',
            '"api modeling and sdk generation"',
            '"fern openapi definition"',
            '"best tool to generate api sdk"',
            '[fern api alternative]'
        ],
        ("Google-Sa-Comp-VSCode-Global", "Thunder-Client"): [
            '"thunder client alternative"',
            '"visual api client like thunder client"',
            '[thunder client alternative]'
        ],
        ("Google-Sa-Comp-VSCode-Global", "REST-Client"): [
            '"vscode rest client alternative"',
            '"api client vscode extension free"',
            '"offline api client for developers"'
        ],
        ("Google-Sa-Design-Global", "Design-Global"): [
            '"api first design tool"',
            '"visual openapi 3 design tool"',
            '"collaborative api modeling platform"',
            '"design api contract before coding"',
            '[api design tool]'
        ],
        ("Google-Sa-Expansion-Horizon-2026", "AG-Postman-Conquest"): [
            '"best api testing and mocking tool"',
            '"all in one api platform for teams"',
            '"postman alternative for agile teams"',
            '"api documentation and mock server"',
            '[api mocking and testing tool]'
        ],
        ("Google-Sa-Testing-Global", "Automated api testing-Global"): [
            '"automated api regression runner"',
            '"no code api testing tool"',
            '"continuous api test automation in cicd"',
            '"api functional testing platform"',
            '[automated api testing tool]'
        ]
    }
    add_expansion_keywords(client, camps_info, expansions_map)
    
    print("\n==================================================")
    print("🎉 [DONE] 全盘零增重构、梯级CPA、否词与拓词方案执行完成！")
    print("==================================================")

if __name__ == "__main__":
    main()
