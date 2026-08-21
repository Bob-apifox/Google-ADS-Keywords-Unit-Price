import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

BUDGET_ADJUSTMENTS = {
    "Google-Sa-Mintlify-Global": 35.0,
    "Google-Sa-Jmeter-Global": 50.0,
    "Google-Sa-Category-Competitor-Global": 25.0,
    "Google-PMax-CP-Global": 35.0
}

NEGATIVE_PACKS = {
    "Google-Sa-Mintlify-Global": [
        ("firebase studio", "PHRASE"),
        ("uvicorn", "PHRASE"),
        ("install dependencies", "PHRASE"),
        ("app para programar", "PHRASE"),
        ("ia experta en programacion", "PHRASE"),
        ("code maker", "PHRASE")
    ],
    "Google-Sa-Jmeter-Global": [
        ("vulnerability online scanner", "PHRASE"),
        ("network testing", "PHRASE"),
        ("internet stability test packet loss", "PHRASE"),
        ("packet loss", "PHRASE"),
        ("keycdn performance test", "PHRASE"),
        ("load time checker", "PHRASE")
    ],
    "Google-Sa-Category-Competitor-Global": [
        ("npm install npm start", "PHRASE"),
        ("node js", "EXACT"),
        ("ngrok", "EXACT")
    ]
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    budget_service = client.get_service("CampaignBudgetService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    print("==========================================================================")
    print("[1. EXECUTING BUDGET CUTS FOR MINTLIFY, JMETER, CATEGORY & PMAX]")
    print("==========================================================================")

    names_str = ", ".join([f"'{n}'" for n in BUDGET_ADJUSTMENTS.keys()])
    q = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.resource_name,
            campaign.campaign_budget
        FROM campaign
        WHERE campaign.name IN ({names_str})
    """
    c_map = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=q):
        for row in batch.results:
            c_map[row.campaign.name] = row.campaign

    for name, target_b in BUDGET_ADJUSTMENTS.items():
        if name not in c_map:
            print(f"[WARN] Campaign '{name}' not found!")
            continue
        c = c_map[name]
        new_b_micros = int(target_b * 1000000)
        b_op = client.get_type("CampaignBudgetOperation")
        b_up = b_op.update
        b_up.resource_name = c.campaign_budget
        b_up.amount_micros = new_b_micros
        client.copy_from(b_op.update_mask, protobuf_helpers.field_mask(None, b_up._pb))

        try:
            budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[b_op])
            print(f"[SUCCESS] [{name}] Budget -> ${target_b:.2f}/day")
        except Exception as e:
            print(f"[ERROR] Updating budget for [{name}]: {e}")

    print("\n==========================================================================")
    print("[2. INJECTING NEGATIVE KEYWORD PACKS (A, B, C)]")
    print("==========================================================================")
    kw_ops = []
    for cname, negs in NEGATIVE_PACKS.items():
        if cname not in c_map:
            continue
        c_res = c_map[cname].resource_name
        for kw_text, match_type in negs:
            op = client.get_type("CampaignCriterionOperation")
            crit = op.create
            crit.campaign = c_res
            crit.negative = True
            crit.keyword.text = kw_text
            crit.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match_type)
            kw_ops.append(op)
            print(f"[{cname}] Negative: [{match_type}] '{kw_text}'")

    if kw_ops:
        try:
            resp = campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=kw_ops)
            print(f"\n[SUCCESS] Successfully injected {len(resp.results)} campaign negative keywords!")
        except Exception as e:
            print(f"\n[ERROR] Injecting negative keywords: {e}")

    print("\n==========================================================================")
    print("[FINISHED] Today's Optimization & Cleanup Execution Complete!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
