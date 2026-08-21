import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

# Target Budget and tCPA adjustments calibrated on 7-Day High ROI Data
BUDGET_ADJUSTMENTS = {
    # 🚀 7 大超低成本暴利王牌系列 (全面加码扩量 +20% ~ +35%)
    "Google-Sa-Jmeter-Global": {"budget_usd": 95.0, "tcpa_usd": 2.50},       # 7天 395.6 转化, CPA $1.40
    "Google-Sa-Readme-Global": {"budget_usd": 75.0, "tcpa_usd": 2.50},       # 7天 216.7 转化, CPA $1.79
    "Google-Sa-Hoppscotch-Global": {"budget_usd": 38.0, "tcpa_usd": 2.50},   # 7天 124.0 转化, CPA $1.60
    "Google-Sa-Fern-Global": {"budget_usd": 48.0, "tcpa_usd": 2.50},         # 7天 80.5 转化, CPA $1.74
    "Google-Sa-API Editor-Global": {"budget_usd": 32.0, "tcpa_usd": 2.50},   # 7天 96.4 转化, CPA $1.54
    "Google-Sa-Func-MultiProtocol-Global": {"budget_usd": 30.0, "tcpa_usd": 2.50}, # 7天 65.5 转化, CPA $1.28
    "Google-Sa-Bruno-Global": {"budget_usd": 15.0, "tcpa_usd": 2.50},        # 7天 35.5 转化, CPA $1.62

    # 🔥 核心保量与重点增量系列
    "Google-Sa-CP-Global": {"budget_usd": 180.0, "tcpa_usd": 2.30},
    "Google-Sa-Postman-Global": {"budget_usd": 95.0, "tcpa_usd": 2.90},
    "Google-Sa-DSA-Alternatives-Global": {"budget_usd": 50.0, "tcpa_usd": 2.50},
    "Google-Sa-Comp-HeavyQA-Global": {"budget_usd": 45.0, "tcpa_usd": 2.50},
    "Google-Sa-Doc-Global": {"budget_usd": 25.0, "tcpa_usd": 2.50},
    "Google-Sa-CP-TW": {"budget_usd": 15.0, "tcpa_usd": 2.50},

    # 🛑 削减抽血系列 (释放资金给暴利王牌)
    "Google-Sa-Solutions-AI-LLM-Global": {"budget_usd": 120.0, "tcpa_usd": 2.50}, # 削减 -$50/天
    "Google-Sa-Insomnia-Global": {"budget_usd": 15.0, "tcpa_usd": 3.00},         # 削减 -$10/天
    "Google-Sa-Stoplight-Global": {"budget_usd": 18.0, "tcpa_usd": 2.80},        # 削减 -$7/天
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    campaign_service = client.get_service("CampaignService")
    budget_service = client.get_service("CampaignBudgetService")

    print("=== Fetching Campaigns to Adjust ===")
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.resource_name,
            campaign.campaign_budget,
            campaign.bidding_strategy_type,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """

    campaign_map = {}
    budget_resource_map = {}
    
    for batch in ga_service.search_stream(customer_id=customer_id, query=query):
        for row in batch.results:
            name = row.campaign.name
            if name in BUDGET_ADJUSTMENTS:
                campaign_map[name] = {
                    "resource_name": row.campaign.resource_name,
                    "budget_resource": row.campaign.campaign_budget,
                    "bidding_type": row.campaign.bidding_strategy_type.name,
                }
                budget_resource_map[row.campaign.campaign_budget] = name

    print(f"Matched {len(campaign_map)} Campaigns out of {len(BUDGET_ADJUSTMENTS)} planned.")

    # 1. Update Budgets
    budget_ops = []
    for budget_res, camp_name in budget_resource_map.items():
        target = BUDGET_ADJUSTMENTS[camp_name]
        amount_micros = int(target["budget_usd"] * 1000000)
        
        op = client.get_type("CampaignBudgetOperation")
        b = op.update
        b.resource_name = budget_res
        b.amount_micros = amount_micros
        client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, b._pb))
        budget_ops.append((camp_name, op, target["budget_usd"]))

    print("\n--- Updating Budgets ---")
    for name, op, b_usd in budget_ops:
        try:
            budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[op])
            print(f"✅ [{name}] Budget updated to ${b_usd:.2f}/day")
        except Exception as e:
            print(f"❌ [{name}] Failed updating budget: {e}")

    # 2. Update Target CPAs on Campaigns
    print("\n--- Updating Target CPAs ---")
    for name, info in campaign_map.items():
        target = BUDGET_ADJUSTMENTS[name]
        tcpa_micros = int(target["tcpa_usd"] * 1000000)
        
        op = client.get_type("CampaignOperation")
        c = op.update
        c.resource_name = info["resource_name"]
        
        # Check bidding strategy
        if "MAXIMIZE_CONVERSIONS" in info["bidding_type"]:
            c.maximize_conversions.target_cpa_micros = tcpa_micros
        else:
            c.target_cpa.target_cpa_micros = tcpa_micros
            
        client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, c._pb))
        try:
            campaign_service.mutate_campaigns(customer_id=customer_id, operations=[op])
            print(f"✅ [{name}] Target CPA updated to ${target['tcpa_usd']:.2f}")
        except Exception as e:
            print(f"❌ [{name}] Failed updating Target CPA: {e}")

    print("\n🎉 All calibrated budget and tCPA adjustments completed successfully!")

if __name__ == '__main__':
    main()
