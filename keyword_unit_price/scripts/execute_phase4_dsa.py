import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'
CAMPAIGN_NAME = 'Google-Sa-DSA-Global'
AD_GROUP_NAME = 'CLI Group'

URLS = [
    'https://apidog.com/blog/lightweight-cli-tools-api-collaboration/',
    'https://apidog.com/blog/apidog-cli-agent-api-documentation/',
    'https://apidog.com/blog/lightweight-cli-tools-api-mocking/',
    'https://apidog.com/blog/lightweight-cli-tools-for-development/',
    'https://apidog.com/blog/lightweight-cli-tools-api-management/',
    'https://apidog.com/blog/lightweight-cli-tools-api-testing/',
    'https://apidog.com/blog/lightweight-cli-tools-api-documentation/',
    'https://apidog.com/blog/open-source-cli-tools-api-documentation/'
]

DESC_1 = "Explore lightweight CLI tools for API testing. Streamline your CI/CD workflow."
DESC_2 = "Discover open-source CLI agents for developers. Automate API testing easily."
TRACKING_TEMPLATE = "{lpurl}?utm_source=google_dsa&utm_medium={network}&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_service = client.get_service("AdGroupService")
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    
    # 1. Find Campaign
    query = f"SELECT campaign.resource_name FROM campaign WHERE campaign.name = '{CAMPAIGN_NAME}' AND campaign.status = 'ENABLED' LIMIT 1"
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    campaign_rn = None
    for batch in stream:
        for row in batch.results:
            campaign_rn = row.campaign.resource_name
            break
            
    if not campaign_rn:
        print(f"Error: Campaign {CAMPAIGN_NAME} not found.")
        return

    try:
        # 2. Check if DSA Ad Group exists
        query_ag = f"SELECT ad_group.resource_name FROM ad_group WHERE campaign.resource_name = '{campaign_rn}' AND ad_group.name = '{AD_GROUP_NAME}' AND ad_group.status = 'ENABLED' LIMIT 1"
        stream_ag = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_ag)
        ad_group_rn = None
        for batch in stream_ag:
            for row in batch.results:
                ad_group_rn = row.ad_group.resource_name
                break
                
        if not ad_group_rn:
            ag_op = client.get_type("AdGroupOperation")
            ad_group = ag_op.create
            ad_group.name = AD_GROUP_NAME
            ad_group.campaign = campaign_rn
            ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS
            ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
            ad_group.tracking_url_template = TRACKING_TEMPLATE
            
            ag_resp = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op])
            ad_group_rn = ag_resp.results[0].resource_name
            print(f"Created NEW DSA Ad Group: {ad_group_rn}")
        else:
            print(f"Found EXISTING DSA Ad Group: {ad_group_rn}")

        # 3. URLs already added successfully in previous run.
        print("URLs already exist in Ad Group.")

        # 4. Create Dynamic Search Ad
        ad_op = client.get_type("AdGroupAdOperation")
        ad = ad_op.create
        ad.ad_group = ad_group_rn
        ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        dsa = ad.ad.expanded_dynamic_search_ad
        dsa.description1 = DESC_1
        dsa.description2 = DESC_2
        
        ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
        print("Created Dynamic Search Ad.")
        
    except GoogleAdsException as ex:
        print(f"Request failed with status '{ex.error.code().name}':")
        for error in ex.failure.errors:
            print(f"\tError: {error.message}")

if __name__ == '__main__':
    main()
