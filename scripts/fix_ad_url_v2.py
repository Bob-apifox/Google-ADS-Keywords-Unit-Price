import os
from google.ads.googleads.client import GoogleAdsClient

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
            ad_group.resource_name,
            ad_group.name, 
            campaign.name,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.ad.responsive_search_ad.descriptions,
            ad_group_ad.ad.responsive_search_ad.path1,
            ad_group_ad.ad.responsive_search_ad.path2,
            ad_group_ad.ad.tracking_url_template
        FROM ad_group_ad 
        WHERE campaign.name = 'Google-Sa-Testing-Global' 
          AND ad_group.name = 'Testing-Security-Auth'
          AND ad_group_ad.status != 'REMOVED'
    """
    
    mutations = []
    
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            print(f"Found Ad in {row.ad_group.name} (Ad ID: {row.ad_group_ad.ad.id})")
            
            old_rsa = row.ad_group_ad.ad.responsive_search_ad
            
            # 1. Create New Ad
            create_op = client.get_type("AdGroupAdOperation")
            new_ad = create_op.create
            new_ad.ad_group = row.ad_group.resource_name
            new_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
            
            new_ad.ad.final_urls.append('https://apidog.com/api-testing/')
            if row.ad_group_ad.ad.tracking_url_template:
                new_ad.ad.tracking_url_template = row.ad_group_ad.ad.tracking_url_template
            
            # Copy headlines
            for h in old_rsa.headlines:
                asset = client.get_type("AdTextAsset")
                asset.text = h.text
                if h.pinned_field:
                    asset.pinned_field = h.pinned_field
                new_ad.ad.responsive_search_ad.headlines.append(asset)
                
            # Copy descriptions
            for d in old_rsa.descriptions:
                asset = client.get_type("AdTextAsset")
                asset.text = d.text
                if d.pinned_field:
                    asset.pinned_field = d.pinned_field
                new_ad.ad.responsive_search_ad.descriptions.append(asset)
                
            if old_rsa.path1:
                new_ad.ad.responsive_search_ad.path1 = old_rsa.path1
            if old_rsa.path2:
                new_ad.ad.responsive_search_ad.path2 = old_rsa.path2

            mutations.append(create_op)
            
            # 2. Remove Old Ad
            remove_op = client.get_type("AdGroupAdOperation")
            remove_op.remove = row.ad_group_ad.resource_name
            mutations.append(remove_op)

    if mutations:
        try:
            resp = ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=mutations)
            print(f"Successfully replaced ads.")
        except Exception as e:
            print(f"Failed to replace ads: {e}")
            if hasattr(e, 'failure'):
                for error in e.failure.errors:
                    print(error.message)
    else:
        print("No active ads found to update.")

if __name__ == '__main__':
    execute()
