import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")
ad_group_ad_service = client.get_service("AdGroupAdService")

campaign_ids = [
    '23981394894', '23981398449', '23990938534', 
    '23986384244', '23990942638', '23981407167', '23981409303'
]

suffix = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

campaign_ids_str = ', '.join(campaign_ids)
query = f"""
    SELECT
      ad_group_ad.ad.id,
      ad_group_ad.ad.final_urls,
      ad_group_ad.ad.responsive_search_ad.headlines,
      ad_group_ad.ad.responsive_search_ad.descriptions,
      ad_group_ad.ad.expanded_dynamic_search_ad.description,
      ad_group_ad.ad.expanded_dynamic_search_ad.description2,
      ad_group_ad.ad.type,
      ad_group_ad.ad_group,
      ad_group.id,
      campaign.id,
      ad_group_ad.resource_name
    FROM ad_group_ad
    WHERE campaign.id IN ({campaign_ids_str})
      AND ad_group_ad.status = 'ENABLED'
"""

print("Fetching ads...")
response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
operations = []

for row in response:
    # 1. Remove old ad
    remove_op = client.get_type("AdGroupAdOperation")
    remove_op.remove = row.ad_group_ad.resource_name
    operations.append(remove_op)
    
    # 2. Create new ad
    create_op = client.get_type("AdGroupAdOperation")
    new_ad = create_op.create
    new_ad.ad_group = row.ad_group_ad.ad_group
    new_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    
    ad = new_ad.ad
    for url in row.ad_group_ad.ad.final_urls:
        ad.final_urls.append(url)
        
    ad.final_url_suffix = suffix

    if row.ad_group_ad.ad.type_ == client.enums.AdTypeEnum.RESPONSIVE_SEARCH_AD:
        rsa = ad.responsive_search_ad
        for h in row.ad_group_ad.ad.responsive_search_ad.headlines:
            new_h = client.get_type("AdTextAsset")
            new_h.text = h.text
            rsa.headlines.append(new_h)
        for d in row.ad_group_ad.ad.responsive_search_ad.descriptions:
            new_d = client.get_type("AdTextAsset")
            new_d.text = d.text
            rsa.descriptions.append(new_d)
            
    elif row.ad_group_ad.ad.type_ == client.enums.AdTypeEnum.EXPANDED_DYNAMIC_SEARCH_AD:
        dsa = ad.expanded_dynamic_search_ad
        dsa.description = row.ad_group_ad.ad.expanded_dynamic_search_ad.description
        if row.ad_group_ad.ad.expanded_dynamic_search_ad.description2:
            dsa.description2 = row.ad_group_ad.ad.expanded_dynamic_search_ad.description2

    operations.append(create_op)

if operations:
    print(f"Found {len(operations)//2} ads to recreate. Executing...")
    for i in range(0, len(operations), 100):
        batch = operations[i:i + 100]
        try:
            mutate_response = ad_group_ad_service.mutate_ad_group_ads(
                customer_id=CUSTOMER_ID, operations=batch
            )
            print(f"Batch {i//100 + 1}: Successfully processed {len(mutate_response.results)} operations.")
        except Exception as e:
            print(f"Error in batch {i//100 + 1}: {e}")
else:
    print("No ads found to recreate.")

print("Done.")
