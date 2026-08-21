import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

CAMPAIGN_IDS = [24126382470, 24131994659]

CONTENT_LABELS_TO_EXCLUDE = [
    "JUVENILE",             # Exclude content suitable for families/children
    "GAMES",                # Exclude gaming content
    "JACKASS",              # Exclude profanity/rough humor
    "TRAGEDY",              # Exclude sensitive tragedy/conflict
    "PARKED_DOMAIN",        # Exclude parked domains
    "BELOW_THE_FOLD",       # Avoid below-the-fold placements
    "VIDEO_NOT_YET_RATED"   # Avoid unrated content
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    for cid in CAMPAIGN_IDS:
        print(f"\n[Injecting Exclusions into Campaign {cid}]")
        ops = []
        for label_name in CONTENT_LABELS_TO_EXCLUDE:
            try:
                op = client.get_type("CampaignCriterionOperation")
                crit = op.create
                crit.campaign = f"customers/{customer_id}/campaigns/{cid}"
                crit.negative = True
                crit.content_label.type_ = getattr(client.enums.ContentLabelTypeEnum, label_name)
                ops.append(op)
            except Exception as e:
                print(f"  Error building {label_name}: {e}")

        if ops:
            try:
                resp = campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=ops)
                print(f"  [SUCCESS] Injected {len(resp.results)} content label exclusions (Games, Juvenile, Parked Domains, Below The Fold) into Campaign {cid}!")
            except Exception as e:
                print(f"  [NOTE] Exclusions mutate: {e}")

if __name__ == '__main__':
    main()
