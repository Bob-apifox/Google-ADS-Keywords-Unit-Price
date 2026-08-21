import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

# 2.1 预算削减与 tCPA 压制清单
BUDGET_TCPA_PUNISHMENTS = {
    "Google-Sa-Stoplight-Global": {"budget_usd": 12.0, "tcpa_usd": 3.00},
    "Google-Sa-Insomnia-Global": {"budget_usd": 12.0, "tcpa_usd": 3.00},
    "Google-Sa-MCP-Infrastructure": {"budget_usd": 10.0, "tcpa_usd": 2.50},
    "Google-Sa-Func-CICD-Global": {"budget_usd": 10.0, "tcpa_usd": 2.50},
    "Google-PMax-Postman": {"budget_usd": 30.0, "tcpa_usd": 4.00},
    "Google-Sa-Jmeter-Global": {"budget_usd": 65.0, "tcpa_usd": 3.50},
    "Google-Sa-Readme-Global": {"budget_usd": 55.0, "tcpa_usd": 3.00},
    "Google-Sa-Solutions-AI-LLM-Global": {"budget_usd": 120.0, "tcpa_usd": 2.50},
}

# 2.2 四大否定词包
NEG_PACK_A = [
    "connect api to cursor",
    "cursor ai alternative",
    "ai code generator for api",
    "ai backend generator",
    "ai schema generator",
    "ai boilerplate generator",
    "ai coding assistant free",
    "dart devtools",
    "chrome debugger",
    "v0 by vercel",
    "bolt new",
    "openhands",
    "aider",
    "openmanus",
    "openrouter",
    "qwen 3.6 coder",
    "deepseek api key free"
]

NEG_PACK_B = [
    "pwa progressive web app",
    "mobile app development",
    "app js",
    "pwabuilder",
    "glide apps",
    "appmachine",
    "andromo",
    "create an app",
    "groupdocs",
    "relume",
    "anthropic console",
    "web design software",
    "web bluetooth api"
]

NEG_PACK_C = [
    "postman download for windows 7",
    "postman crack",
    "postman student project",
    "postman homework assignment",
    "postman download without login",
    "thunder client crack",
    "insomnia download 32 bit",
    "free api key generator",
    "api tutorial for beginners"
]

NEG_PACK_D = [
    "api sprawl",
    "api create online",
    "api vulnerability scanner",
    "automated test case generation",
    "httpie alternative free",
    "main py",
    "run code online",
    "jsbin",
    "codepad",
    "performance load testing"
]

CAMPAIGN_NEG_MAPPINGS = {
    # 词包 A 目标系列
    "Google-Sa-Solutions-AI-LLM-Global": NEG_PACK_A,
    "Google-Sa-DSA-Global": NEG_PACK_A,
    
    # 词包 B 目标系列
    "Google-Sa-Insomnia-Global": NEG_PACK_B,
    "Google-Sa-Stoplight-Global": NEG_PACK_B,
    
    # 词包 C 目标系列
    "Google-Sa-Postman-Global": NEG_PACK_C,
    "Google-Sa-CP-Global": NEG_PACK_C,
    "Google-Sa-CP-AR": NEG_PACK_C,
    
    # 词包 D 目标系列
    "Google-Sa-Jmeter-Global": NEG_PACK_D,
    "Google-Sa-API Editor-Global": NEG_PACK_D,
    "Google-Sa-Design-Global": NEG_PACK_D
}

def execute_part_2_1_and_2_2():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    campaign_service = client.get_service("CampaignService")
    budget_service = client.get_service("CampaignBudgetService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    print("==========================================================================")
    print("[STARTING] Part 2.1 Budget/tCPA Punishments & Part 2.2 Negative Keywords Injection")
    print("==========================================================================")

    # 1. 查找所有涉及的 Campaign 资源名称
    all_campaign_names = set(BUDGET_TCPA_PUNISHMENTS.keys()).union(set(CAMPAIGN_NEG_MAPPINGS.keys()))
    names_str = ", ".join([f"'{n}'" for n in all_campaign_names])
    
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.resource_name,
            campaign.campaign_budget,
            campaign.bidding_strategy_type,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros
        FROM campaign
        WHERE campaign.name IN ({names_str})
    """
    
    campaign_map = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=query):
        for row in batch.results:
            campaign_map[row.campaign.name] = row.campaign

    print(f"Found {len(campaign_map)} Campaigns in Google Ads.")

    # -------------------------------------------------------------------------
    # 执行 2.1: 预算削减与 tCPA 调整
    # -------------------------------------------------------------------------
    print("\n--- [2.1] Executing Budget Reductions & Target CPA Adjustments ---")
    for name, params in BUDGET_TCPA_PUNISHMENTS.items():
        if name not in campaign_map:
            print(f"Campaign '{name}' not found, skipping.")
            continue
        c = campaign_map[name]
        
        # 1. 预算更新
        new_budget_micros = int(params["budget_usd"] * 1000000)
        b_op = client.get_type("CampaignBudgetOperation")
        b_update = b_op.update
        b_update.resource_name = c.campaign_budget
        b_update.amount_micros = new_budget_micros
        client.copy_from(b_op.update_mask, protobuf_helpers.field_mask(None, b_update._pb))

        # 2. Target CPA 更新
        new_tcpa_micros = int(params["tcpa_usd"] * 1000000)
        c_op = client.get_type("CampaignOperation")
        c_update = c_op.update
        c_update.resource_name = c.resource_name
        if "MAXIMIZE_CONVERSIONS" in c.bidding_strategy_type.name:
            c_update.maximize_conversions.target_cpa_micros = new_tcpa_micros
        else:
            c_update.target_cpa.target_cpa_micros = new_tcpa_micros
        client.copy_from(c_op.update_mask, protobuf_helpers.field_mask(None, c_update._pb))

        try:
            budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[b_op])
            campaign_service.mutate_campaigns(customer_id=customer_id, operations=[c_op])
            print(f"[SUCCESS] [{name}] Budget -> ${params['budget_usd']:.2f}/day | Target CPA -> ${params['tcpa_usd']:.2f}")
        except Exception as e:
            print(f"[ERROR] updating [{name}]: {e}")

    # -------------------------------------------------------------------------
    # 执行 2.2: 注入 Campaign 级否定关键词
    # -------------------------------------------------------------------------
    print("\n--- [2.2] Executing Campaign-Level Negative Keywords Injection ---")
    
    # 先查询现有的否定词，避免重复添加导致报错
    existing_negatives = {}
    neg_query = """
        SELECT
            campaign.name,
            campaign_criterion.keyword.text
        FROM campaign_criterion
        WHERE campaign_criterion.type = 'KEYWORD'
          AND campaign_criterion.negative = TRUE
    """
    for batch in ga_service.search_stream(customer_id=customer_id, query=neg_query):
        for row in batch.results:
            c_name = row.campaign.name
            kw = row.campaign_criterion.keyword.text.lower()
            if c_name not in existing_negatives:
                existing_negatives[c_name] = set()
            existing_negatives[c_name].add(kw)

    for c_name, keywords in CAMPAIGN_NEG_MAPPINGS.items():
        if c_name not in campaign_map:
            print(f"Campaign '{c_name}' not found for negatives, skipping.")
            continue
        c_resource = campaign_map[c_name].resource_name
        exist_set = existing_negatives.get(c_name, set())

        operations = []
        added_kws = []
        for kw in keywords:
            if kw.lower() in exist_set:
                continue
            
            crit_op = client.get_type("CampaignCriterionOperation")
            crit = crit_op.create
            crit.campaign = c_resource
            crit.negative = True
            crit.keyword.text = kw
            crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            operations.append(crit_op)
            added_kws.append(kw)

        if operations:
            try:
                campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=operations)
                print(f"[SUCCESS] [{c_name}] Injected {len(operations)} Negative Keywords: {added_kws[:3]}...")
            except Exception as e:
                print(f"[ERROR] [{c_name}] Negative keyword injection error: {e}")
        else:
            print(f"[INFO] [{c_name}] All negative keywords already exist.")

    print("\n==========================================================================")
    print("[FINISHED] 2.1 Budget Punishments & 2.2 Negative Cleanups Successfully Applied!")
    print("==========================================================================")

if __name__ == '__main__':
    execute_part_2_1_and_2_2()
