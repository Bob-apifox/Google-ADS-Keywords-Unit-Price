import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

SCALING_CAMPAIGNS = {
    "Google-Sa-Expansion-Horizon-2026": {"budget_usd": 50.0, "tcpa_usd": 2.70},
    "Google-Sa-Debug-Global": {"budget_usd": 40.0, "tcpa_usd": 2.50},
    "Google-Sa-Mock-Global": {"budget_usd": 55.0, "tcpa_usd": 3.00},
    "Google-Sa-Solutions-Unified-API-Global": {"budget_usd": 35.0, "tcpa_usd": 2.50},
    "Google-Sa-CP-JP": {"budget_usd": 20.0, "tcpa_usd": 3.00},
    "Google-Sa-CP-KR": {"budget_usd": 20.0, "tcpa_usd": 2.80}
}

EXACT_KEYWORDS_TO_HARVEST = {
    "Google-Sa-Mock-Global": [
        ("mock api for frontend development", "EXACT"),
        ("mock api for frontend development", "PHRASE"),
        ("api mocking and testing tool", "EXACT"),
        ("mock api frontend", "PHRASE")
    ],
    "Google-Sa-Solutions-Unified-API-Global": [
        ("unified api platform", "EXACT"),
        ("unified api platform", "PHRASE"),
        ("all in one api platform", "EXACT"),
        ("all in one api platform", "PHRASE")
    ]
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    campaign_service = client.get_service("CampaignService")
    budget_service = client.get_service("CampaignBudgetService")
    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    print("==========================================================================")
    print("[1. EXECUTING BUDGET UNCAP & TARGET CPA LIBERATION FOR SCALING CAMPAIGNS]")
    print("==========================================================================")

    names_str = ", ".join([f"'{n}'" for n in SCALING_CAMPAIGNS.keys()])
    q = f"""
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
    c_map = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=q):
        for row in batch.results:
            c_map[row.campaign.name] = row.campaign

    for name, target in SCALING_CAMPAIGNS.items():
        if name not in c_map:
            print(f"[WARN] Campaign '{name}' not found!")
            continue
        c = c_map[name]

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
            print(f"[SUCCESS] [{name}] -> Budget: ${target['budget_usd']:.2f}/day | Target CPA: ${target['tcpa_usd']:.2f}")
        except Exception as e:
            print(f"[ERROR] Updating [{name}]: {e}")

    print("\n==========================================================================")
    print("[2. CLEARING AD GROUP OVERRIDES IN SCALING CAMPAIGNS]")
    print("==========================================================================")
    ag_q = f"""
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
    for batch in ga_service.search_stream(customer_id=customer_id, query=ag_q):
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
            ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=ag_ops)
            print(f"[SUCCESS] Cleared {len(ag_ops)} Ad Group overrides for clean inheritance!")
        except Exception as e:
            print(f"[ERROR] Clearing Ad Group overrides: {e}")
    else:
        print("[INFO] All Ad Groups already cleanly inherit.")

    print("\n==========================================================================")
    print("[3. HARVESTING HIGH-CONVERTING SEARCH TERMS AS EXACT & PHRASE KEYWORDS]")
    print("==========================================================================")
    # Find primary enabled Ad Group for Mock and Unified API
    ag_find_q = """
        SELECT ad_group.id, ad_group.name, ad_group.resource_name, campaign.name
        FROM ad_group
        WHERE campaign.name IN ('Google-Sa-Mock-Global', 'Google-Sa-Solutions-Unified-API-Global')
          AND ad_group.status = 'ENABLED'
    """
    primary_ags = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=ag_find_q):
        for row in batch.results:
            cname = row.campaign.name
            if cname not in primary_ags:
                primary_ags[cname] = row.ad_group.resource_name

    kw_ops = []
    for cname, kws in EXACT_KEYWORDS_TO_HARVEST.items():
        if cname not in primary_ags:
            print(f"[WARN] No enabled Ad Group in '{cname}'")
            continue
        ag_res = primary_ags[cname]
        for kw_text, match_type in kws:
            op = client.get_type("AdGroupCriterionOperation")
            crit = op.create
            crit.ad_group = ag_res
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            crit.keyword.text = kw_text
            crit.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match_type)
            kw_ops.append(op)
            print(f"[{cname}] Added Keyword: [{match_type}] '{kw_text}'")

    if kw_ops:
        try:
            resp = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=kw_ops)
            print(f"\n[SUCCESS] Successfully harvested {len(resp.results)} high-converting keywords!")
        except Exception as e:
            print(f"\n[ERROR] Harvesting keywords: {e}")

    print("\n==========================================================================")
    print("[FINISHED] Scaling & Expansion Plan Successfully Executed Online!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
