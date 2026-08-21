import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service('GoogleAdsService')
ad_group_ad_service = client.get_service('AdGroupAdService')

c_id = '23981394894'
ag_name = 'REST-Client'

# Fetch the Ad Group ID
query = f'''
    SELECT ad_group.id
    FROM ad_group
    WHERE campaign.id = {c_id} AND ad_group.name = '{ag_name}'
'''
stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
ag_id = None
for batch in stream:
    for row in batch.results:
        ag_id = row.ad_group.id

if not ag_id:
    print("Ad group not found.")
else:
    print(f"Found REST-Client Ad Group ID: {ag_id}")
    ag_resource_name = client.get_service('AdGroupService').ad_group_path(CUSTOMER_ID, ag_id)
    
    # Inject Ad
    ad_op = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_op.create
    ad_group_ad.ad_group = ag_resource_name
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    
    ad = ad_group_ad.ad
    ad.final_urls.append("https://apidog.com/")
    
    rsa = ad.responsive_search_ad
    
    # Fixed the headline length! "VS Code REST Client Alternative" (31) -> "REST Client Alternative" (23)
    headlines = ["REST Client Alternative", "Better API Client", "Switch to Apidog Today", "Advanced API Testing Tool", "Free API Client"]
    for text in headlines:
        h = client.get_type("AdTextAsset")
        h.text = text
        rsa.headlines.append(h)
        
    descriptions = ["Upgrade from simple extensions. Get a unified workspace for API Design and Mocking.", "Stop struggling with simple extensions. Import data in 1 click and automate tests.", "Join 1,000,000+ developers using Apidog for a faster workflow."]
    for text in descriptions:
        d = client.get_type("AdTextAsset")
        d.text = text
        rsa.descriptions.append(d)
        
    try:
        ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
        print("Success: Injected the missing RSA for REST-Client.")
    except Exception as e:
        print(f"Error: {e}")

