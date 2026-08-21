import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

def execute():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    ad_group_ad_service = client.get_service('AdGroupAdService')

    query = """
        SELECT 
            ad_group_ad.ad.id, 
            ad_group_ad.resource_name,
            ad_group.name, 
            campaign.name
        FROM ad_group_ad 
        WHERE campaign.name = 'Google-Sa-Testing-Global' 
          AND ad_group.name = 'Testing-Security-Auth'
    """
    
    ad_ops = []
    
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            print(f"Found Ad in {row.ad_group.name} (Ad ID: {row.ad_group_ad.ad.id})")
            
            # Create the operation
            ad_op = client.get_type("AdGroupAdOperation")
            ad = ad_op.update
            ad.resource_name = row.ad_group_ad.resource_name
            ad.ad.final_urls.append('https://apidog.com/api-testing/')
            
            ad_op.update_mask.paths.append("ad.final_urls")
            ad_ops.append(ad_op)

    if ad_ops:
        try:
            resp = ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=ad_ops)
            print(f"Successfully updated {len(resp.results)} ads.")
        except Exception as e:
            print(f"Failed to update ads: {e}")
    else:
        print("No ads found to update.")

if __name__ == '__main__':
    execute()
