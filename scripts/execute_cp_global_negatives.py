import os
import sys
import urllib3
from google.ads.googleads.client import GoogleAdsClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ["GOOGLE_ADS_USE_REST"] = "true"
sys.stdout.reconfigure(encoding='utf-8')

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'
CP_GLOBAL_ID = '21950794503'

negatives = [
    # High-CPC waste terms identified in CP-Global
    ("github", "BROAD"),
    ("devexpress", "BROAD"),
    ("appsheet", "BROAD"),
    ("claude", "BROAD"),
    ("json query", "BROAD"),
    ("bytez", "BROAD"),
    ("apidog ai", "EXACT"),
    ("apidog free", "EXACT"),
    ("can claude make software", "EXACT"),
    ("claude dashboard templates", "EXACT")
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    cc_service = client.get_service("CampaignCriterionService")
    
    operations = []
    for kw, match_type in negatives:
        operation = client.get_type("CampaignCriterionOperation")
        criterion = operation.create
        criterion.campaign = ga_service.campaign_path(CUSTOMER_ID, CP_GLOBAL_ID)
        criterion.negative = True
        criterion.keyword.text = kw
        if match_type == 'EXACT':
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
        elif match_type == 'PHRASE':
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        else:
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        operations.append(operation)

    req = client.get_type("MutateCampaignCriteriaRequest")
    req.customer_id = CUSTOMER_ID
    req.operations.extend(operations)
    req.partial_failure = True
    
    try:
        res = cc_service.mutate_campaign_criteria(request=req)
        print(f"✅ Successfully added {len(operations)} negative keywords to Google-Sa-CP-Global!")
    except Exception as e:
        print(f"Error adding negative keywords: {e}")

if __name__ == '__main__':
    main()
