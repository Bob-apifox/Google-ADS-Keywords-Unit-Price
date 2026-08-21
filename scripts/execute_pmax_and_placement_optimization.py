import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

# 1. Placement Exclusions (Domains to exclude at Customer/Account Level)
JUNK_PLACEMENT_DOMAINS = [
    "typingtest.com",
    "softonic.com",
    "edclub.com",
    "playgama.com",
    "favninja.com",
    "poki.com",
    "y8.com",
    "friv.com",
    "1vgames.com",
    "sgamer.net",
    "fruitshappy.com",
    "allofapk.com",
    "uptodown.com",
    "gamesxf.com",
    "hoopgame.net",
    "reviewed.app",
    "sarkariresult.com.cm"
]

# 2. Specific Search Campaign Negative Keywords
CAMPAIGN_NEGATIVES = {
    "Google-Sa-Mintlify-Global": [
        ("draw io", "PHRASE"),
        ("app for web development", "PHRASE"),
        ("api rest", "EXACT"),
        ("draw.io", "PHRASE")
    ],
    "Google-Sa-CLI-Terminal-Global": [
        ("replit agent", "PHRASE"),
        ("ai code runner", "PHRASE"),
        ("postman download", "PHRASE"),
        ("postman online", "PHRASE")
    ],
    "Google-Sa-API Editor-Global": [
        ("team api design tool", "PHRASE"),
        ("free online editor", "PHRASE"),
        ("online openapi editor", "PHRASE")
    ],
    "Google-Sa-Openapi-Global": [
        ("software", "EXACT")
    ]
}

# 3. PMax Junk Search Terms (to inject via Campaign Negative Criterion or Shared Set)
PMAX_JUNK_TERMS = [
    ("crack", "BROAD"),
    ("apk", "BROAD"),
    ("free download", "PHRASE"),
    ("typing test", "PHRASE"),
    ("game", "BROAD"),
    ("games", "BROAD"),
    ("poki", "BROAD"),
    ("softonic", "BROAD"),
    ("y8", "BROAD"),
    ("friv", "BROAD"),
    ("edclub", "BROAD")
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    campaign_service = client.get_service("CampaignService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    customer_negative_criterion_service = client.get_service("CustomerNegativeCriterionService")

    print("==========================================================================")
    print("[1. PAUSING GOOGLE-PMAX-POSTMAN (CAMPAIGN ID: 23685533966)]")
    print("==========================================================================")
    
    # Pause Google-PMax-Postman
    c_op = client.get_type("CampaignOperation")
    c_up = c_op.update
    c_up.resource_name = campaign_service.campaign_path(customer_id, "23685533966")
    c_up.status = client.enums.CampaignStatusEnum.PAUSED
    client.copy_from(c_op.update_mask, protobuf_helpers.field_mask(None, c_up._pb))
    
    try:
        campaign_service.mutate_campaigns(customer_id=customer_id, operations=[c_op])
        print("[SUCCESS] Successfully PAUSED Google-PMax-Postman (23685533966)!")
    except Exception as e:
        print(f"[ERROR] Failed to pause Google-PMax-Postman: {e}")

    print("\n==========================================================================")
    print("[2. EXCLUDING JUNK GAME & DOWNLOAD PLACEMENTS AT ACCOUNT LEVEL]")
    print("==========================================================================")
    
    # Query existing customer negative placements to avoid duplicate errors
    q_existing_placements = """
        SELECT customer_negative_criterion.id, customer_negative_criterion.placement.url
        FROM customer_negative_criterion
        WHERE customer_negative_criterion.type = 'PLACEMENT'
    """
    existing_placements = set()
    for batch in ga_service.search_stream(customer_id=customer_id, query=q_existing_placements):
        for row in batch.results:
            existing_placements.add(row.customer_negative_criterion.placement.url.lower())

    placement_ops = []
    for domain in JUNK_PLACEMENT_DOMAINS:
        if domain.lower() in existing_placements:
            print(f"[INFO] Domain '{domain}' already excluded.")
            continue
        op = client.get_type("CustomerNegativeCriterionOperation")
        crit = op.create
        crit.type_ = client.enums.CriterionTypeEnum.PLACEMENT
        crit.placement.url = domain
        placement_ops.append(op)
        print(f"[QUEUED] Account-level exclusion for domain: {domain}")

    if placement_ops:
        try:
            resp = customer_negative_criterion_service.mutate_customer_negative_criteria(
                customer_id=customer_id, operations=placement_ops
            )
            print(f"[SUCCESS] Added {len(resp.results)} account-wide Placement Exclusions!")
        except Exception as e:
            print(f"[ERROR] Adding placement exclusions: {e}")
    else:
        print("[INFO] All junk domains already excluded at account level.")

    print("\n==========================================================================")
    print("[3. INJECTING SEARCH & PMAX CAMPAIGN NEGATIVE KEYWORDS]")
    print("==========================================================================")
    
    # Query campaigns map
    all_c_names = list(CAMPAIGN_NEGATIVES.keys()) + ["Google-PMax-CP-Global"]
    names_str = ", ".join([f"'{n}'" for n in all_c_names])
    q_c = f"SELECT campaign.id, campaign.name, campaign.resource_name FROM campaign WHERE campaign.name IN ({names_str})"
    c_map = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=q_c):
        for row in batch.results:
            c_map[row.campaign.name] = row.campaign.resource_name

    kw_ops = []
    # Search campaign negatives
    for cname, kw_list in CAMPAIGN_NEGATIVES.items():
        if cname not in c_map:
            print(f"[WARN] Campaign '{cname}' not found!")
            continue
        c_res = c_map[cname]
        for kw_text, match_type in kw_list:
            op = client.get_type("CampaignCriterionOperation")
            crit = op.create
            crit.campaign = c_res
            crit.negative = True
            crit.keyword.text = kw_text
            crit.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match_type)
            kw_ops.append(op)
            print(f"[{cname}] Negative: [{match_type}] '{kw_text}'")

    # PMax campaign negatives
    if "Google-PMax-CP-Global" in c_map:
        pmax_res = c_map["Google-PMax-CP-Global"]
        for kw_text, match_type in PMAX_JUNK_TERMS:
            op = client.get_type("CampaignCriterionOperation")
            crit = op.create
            crit.campaign = pmax_res
            crit.negative = True
            crit.keyword.text = kw_text
            crit.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match_type)
            kw_ops.append(op)
            print(f"[Google-PMax-CP-Global] PMax Negative: [{match_type}] '{kw_text}'")

    if kw_ops:
        try:
            resp = campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=kw_ops)
            print(f"\n[SUCCESS] Successfully injected {len(resp.results)} campaign-level negative keywords!")
        except Exception as e:
            print(f"\n[ERROR] Injecting campaign negative criteria: {e}")

    print("\n==========================================================================")
    print("[FINISHED] PMax Pause, Placement Exclusions & Negatives Execution Complete!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
