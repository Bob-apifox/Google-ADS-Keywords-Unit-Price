import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'
CAMPAIGN_NAME = 'Google-Sa-CLI-Global'

NEW_KEYWORDS = [
    'ci cd api testing cli', 'jenkins api test runner', 'github actions api testing', 'gitlab ci api mock',
    'headless api testing tool', 'command line rest client', 'terminal based api client', 'cli tool for api mocking',
    'newman cli alternative', 'curl alternative for api testing', 'httpie alternative'
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    
    # 1. Find the first enabled ad group in the campaign
    query = f"SELECT ad_group.resource_name, ad_group.name FROM ad_group WHERE campaign.name = '{CAMPAIGN_NAME}' AND ad_group.status = 'ENABLED' LIMIT 1"
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    ad_group_rn = None
    for batch in stream:
        for row in batch.results:
            ad_group_rn = row.ad_group.resource_name
            print(f"Found Ad Group: {row.ad_group.name}")
            break
            
    if not ad_group_rn:
        print("No enabled Ad Group found in this campaign.")
        return

    # 2. Add keywords
    operations = []
    for kw in NEW_KEYWORDS:
        op = client.get_type("AdGroupCriterionOperation")
        criterion = op.create
        criterion.ad_group = ad_group_rn
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = kw
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        operations.append(op)
        
    request = client.get_type("MutateAdGroupCriteriaRequest")
    request.customer_id = CUSTOMER_ID
    request.operations = operations
    request.partial_failure = True
    
    ad_group_criterion_service.mutate_ad_group_criteria(request=request)
    print(f"Successfully added {len(NEW_KEYWORDS)} CLI keywords to {CAMPAIGN_NAME}")

if __name__ == "__main__":
    main()
