import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

FINAL_6_CAMPAIGNS = {
    "Google-Sa-CP-Global": {"budget_usd": 180.0, "tcpa_usd": 2.30},
    "Google-Sa-Postman-Global": {"budget_usd": 95.0, "tcpa_usd": 2.90},
    "Google-Sa-Hoppscotch-Global": {"budget_usd": 30.0, "tcpa_usd": 2.50},
    "Google-Sa-Category-Competitor-Global": {"budget_usd": 35.0, "tcpa_usd": 2.50},
    "Google-Sa-CP-TW": {"budget_usd": 15.0, "tcpa_usd": 2.50},
    "Google-PMax-CP-Global": {"budget_usd": 50.0, "tcpa_usd": 3.50}
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    campaign_service = client.get_service("CampaignService")
    budget_service = client.get_service("CampaignBudgetService")
    ad_group_service = client.get_service("AdGroupService")

    print("==========================================================================")
    print("[STARTING] Executing Final 6 Campaigns Budget & Target CPA Alignment")
    print("==========================================================================")

    names_str = ", ".join([f"'{n}'" for n in FINAL_6_CAMPAIGNS.keys()])
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

    # 1. Update Budgets and Target CPAs
    for name, target in FINAL_6_CAMPAIGNS.items():
        if name not in campaign_map:
            print(f"[WARN] Campaign '{name}' not found!")
            continue
        c = campaign_map[name]

        # Budget Update
        new_budget_micros = int(target["budget_usd"] * 1000000)
        b_op = client.get_type("CampaignBudgetOperation")
        b_up = b_op.update
        b_up.resource_name = c.campaign_budget
        b_up.amount_micros = new_budget_micros
        client.copy_from(b_op.update_mask, protobuf_helpers.field_mask(None, b_up._pb))

        # Target CPA Update
        new_tcpa_micros = int(target["tcpa_usd"] * 1000000)
        c_op = client.get_type("CampaignOperation")
        c_up = c_op.update
        c_up.resource_name = c.resource_name
        if "MAXIMIZE_CONVERSIONS" in c.bidding_strategy_type.name:
            c_up.maximize_conversions.target_cpa_micros = new_tcpa_micros
        else:
            c_up.target_cpa.target_cpa_micros = new_tcpa_micros
        client.copy_from(c_op.update_mask, protobuf_helpers.field_mask(None, c_up._pb))

        try:
            budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[b_op])
            campaign_service.mutate_campaigns(customer_id=customer_id, operations=[c_op])
            print(f"[SUCCESS] [{name}] Budget -> ${target['budget_usd']:.2f}/day | Target CPA -> ${target['tcpa_usd']:.2f}")
        except Exception as e:
            print(f"[ERROR] Updating [{name}]: {e}")

    # 2. Clear Ad Group Level Overrides for these campaigns so new Target CPA permeates
    ag_query = f"""
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.resource_name,
            campaign.name
        FROM ad_group
        WHERE campaign.name IN ({names_str})
          AND ad_group.status != 'REMOVED'
          AND ad_group.target_cpa_micros > 0
    """
    ag_ops = []
    for batch in ga_service.search_stream(customer_id=customer_id, query=ag_query):
        for row in batch.results:
            ag_op = client.get_type("AdGroupOperation")
            ag = ag_op.update
            ag.resource_name = row.ad_group.resource_name
            client.copy_from(ag_op.update_mask, protobuf_helpers.field_mask(None, client.get_type("AdGroup")._pb))
            ag_op.update_mask.paths.append("target_cpa_micros")
            ag_ops.append(ag_op)
            print(f"  └─ Clearing override on [{row.campaign.name}] -> {row.ad_group.name}")

    if ag_ops:
        try:
            resp = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=ag_ops)
            print(f"[SUCCESS] Cleared {len(resp.results)} Ad Group level overrides for full inheritance!")
        except Exception as e:
            print(f"[ERROR] Clearing Ad Group overrides: {e}")
    else:
        print("[INFO] All Ad Groups already inherit cleanly.")

    print("\n==========================================================================")
    print("[FINISHED] All 6 Campaigns Successfully Updated & Aligned!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
