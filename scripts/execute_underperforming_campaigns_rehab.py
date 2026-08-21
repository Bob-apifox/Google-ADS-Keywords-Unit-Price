import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

REHAB_CONFIG = {
    "Google-Sa-Stoplight-Global": {
        "budget": 12.0,
        "tcpa": 3.0,
        "negatives": [
            ("stoplight", "EXACT"),
            ("stop light", "EXACT"),
            ("traffic", "PHRASE"),
            ("traffic light", "PHRASE"),
            ("traffic app", "PHRASE"),
            ("stop light traffic tool", "PHRASE")
        ]
    },
    "Google-Sa-Readme-Global": {
        "budget": 30.0,
        "tcpa": 3.0,
        "negatives": [
            ("readme", "EXACT"),
            ("readme.md", "PHRASE"),
            ("github readme", "PHRASE"),
            ("readme template", "PHRASE"),
            ("readme generator", "PHRASE"),
            ("markdown", "PHRASE"),
            ("profile readme", "PHRASE"),
            ("github profile", "PHRASE")
        ]
    },
    "Google-Sa-Insomnia-Global": {
        "budget": 10.0,
        "tcpa": 2.80,
        "negatives": [
            ("sleep", "PHRASE"),
            ("sleep tracker", "PHRASE"),
            ("insomnia cure", "PHRASE"),
            ("insomnia treatment", "PHRASE"),
            ("crack", "PHRASE"),
            ("portable", "PHRASE"),
            ("github release", "PHRASE")
        ]
    },
    "Google-Sa-Bruno-Global": {
        "budget": 10.0,
        "tcpa": 2.80,
        "negatives": [
            ("bruno", "EXACT"),
            ("bruno mars", "PHRASE"),
            ("movie", "PHRASE"),
            ("lyrics", "PHRASE"),
            ("song", "PHRASE")
        ]
    },
    "Google-Sa-CLI-Global": {
        "budget": 8.0,
        "tcpa": 2.80,
        "negatives": [
            ("curl download", "PHRASE"),
            ("curl online", "PHRASE"),
            ("powershell curl", "PHRASE"),
            ("curl windows", "PHRASE")
        ]
    },
    "Google-Sa-CLI-Terminal-Global": {
        "budget": 10.0,
        "tcpa": 2.80,
        "negatives": [
            ("powershell curl", "PHRASE"),
            ("curl command", "PHRASE"),
            ("terminal command", "PHRASE"),
            ("cmd command", "PHRASE")
        ]
    }
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    campaign_service = client.get_service("CampaignService")
    budget_service = client.get_service("CampaignBudgetService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    print("==========================================================================")
    print("[1. EXECUTING BUDGETS & TARGET CPA UPDATES FOR 6 CAMPAIGNS]")
    print("==========================================================================")
    names_str = ", ".join([f"'{n}'" for n in REHAB_CONFIG.keys()])
    q = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.resource_name,
            campaign.campaign_budget,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros
        FROM campaign
        WHERE campaign.name IN ({names_str})
    """
    c_map = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=q):
        for row in batch.results:
            c_map[row.campaign.name] = row.campaign

    # Update budgets and tCPA
    for name, cfg in REHAB_CONFIG.items():
        if name not in c_map:
            print(f"[WARN] Campaign '{name}' not found!")
            continue
        c = c_map[name]
        
        # 1. Budget
        b_op = client.get_type("CampaignBudgetOperation")
        b_up = b_op.update
        b_up.resource_name = c.campaign_budget
        b_up.amount_micros = int(cfg["budget"] * 1000000)
        client.copy_from(b_op.update_mask, protobuf_helpers.field_mask(None, b_up._pb))
        try:
            budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[b_op])
            print(f"[{name:<30}] Budget -> ${cfg['budget']:.2f}/day")
        except Exception as e:
            print(f"[{name}] Budget update error: {e}")

        # 2. Target CPA
        c_op = client.get_type("CampaignOperation")
        c_up = c_op.update
        c_up.resource_name = c.resource_name
        if c.maximize_conversions.target_cpa_micros or not c.target_cpa.target_cpa_micros:
            c_up.maximize_conversions.target_cpa_micros = int(cfg["tcpa"] * 1000000)
        else:
            c_up.target_cpa.target_cpa_micros = int(cfg["tcpa"] * 1000000)
        client.copy_from(c_op.update_mask, protobuf_helpers.field_mask(None, c_up._pb))
        try:
            campaign_service.mutate_campaigns(customer_id=customer_id, operations=[c_op])
            print(f"[{name:<30}] Target CPA -> ${cfg['tcpa']:.2f}")
        except Exception as e:
            print(f"[{name}] Target CPA update error: {e}")

    print("\n==========================================================================")
    print("[2. INJECTING NEGATIVE KEYWORD PACKS FOR 6 CAMPAIGNS]")
    print("==========================================================================")
    kw_ops = []
    for cname, cfg in REHAB_CONFIG.items():
        if cname not in c_map:
            continue
        c_res = c_map[cname].resource_name
        for kw_text, match_type in cfg["negatives"]:
            op = client.get_type("CampaignCriterionOperation")
            crit = op.create
            crit.campaign = c_res
            crit.negative = True
            crit.keyword.text = kw_text
            crit.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match_type)
            kw_ops.append(op)
            print(f"[{cname:<30}] Negative: [{match_type:<6}] '{kw_text}'")

    if kw_ops:
        try:
            resp = campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=[kw_ops[i:i+50] for i in range(0, len(kw_ops), 50)][0])
            print(f"\n[SUCCESS] Successfully injected {len(resp.results)} campaign negative keywords!")
        except Exception as e:
            print(f"\n[ERROR] Injecting negative keywords: {e}")

    print("\n==========================================================================")
    print("[ALL DONE] 6 Underperforming Campaigns Optimized & Purified Live!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
