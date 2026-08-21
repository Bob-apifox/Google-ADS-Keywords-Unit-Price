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
    '23981394894',
    '23981398449',
    '23990938534',
    '23986384244',
    '23990942638',
    '23981407167',
    '23981409303'
]

suffix = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

campaign_ids_str = ', '.join(campaign_ids)
query = f"""
    SELECT
      ad_group_ad.ad.id,
      ad_group_ad.ad.final_url_suffix,
      ad_group_ad.ad_group,
      ad_group.id,
      campaign.id
    FROM ad_group_ad
    WHERE campaign.id IN ({campaign_ids_str})
      AND ad_group_ad.status = 'ENABLED'
"""

print("Fetching ads...")
response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
operations = []

for row in response:
    ad_id = row.ad_group_ad.ad.id
    ad_group_id = row.ad_group.id
    
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.update
    ad_group_ad.resource_name = ad_group_ad_service.ad_group_ad_path(CUSTOMER_ID, ad_group_id, ad_id)
    
    ad_group_ad.ad.resource_name = client.get_service("AdService").ad_path(CUSTOMER_ID, ad_id)
    
    # We update final_url_suffix
    ad_group_ad.ad.final_url_suffix = suffix
    # Clear tracking url template if it was there by mistake
    ad_group_ad.ad.tracking_url_template = ""
    
    client.copy_from(ad_group_ad_operation.update_mask, protobuf_helpers.field_mask(None, ad_group_ad._pb))
    operations.append(ad_group_ad_operation)

if operations:
    print(f"Found {len(operations)} ads. Updating...")
    # Process in batches of 100 to avoid any limits (though 7 campaigns probably won't have too many ads)
    batch_size = 100
    for i in range(0, len(operations), batch_size):
        batch = operations[i:i + batch_size]
        try:
            mutate_response = ad_group_ad_service.mutate_ad_group_ads(
                customer_id=CUSTOMER_ID, operations=batch
            )
            print(f"Batch {i//batch_size + 1}: Successfully updated {len(mutate_response.results)} ads.")
        except Exception as e:
            print(f"Error updating batch {i//batch_size + 1}: {e}")
else:
    print("No ads found to update.")

print("Done.")
