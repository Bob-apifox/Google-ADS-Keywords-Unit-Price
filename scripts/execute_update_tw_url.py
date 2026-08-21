import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'
NEW_TW_URL = "https://apidog.com/zh/compare/apidog-vs-postman/"

def update_tw_url():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    ad_service = client.get_service('AdService')
    
    q_ads = """
        SELECT ad_group_ad.ad.id, ad_group.id, campaign.name, ad_group.name, ad_group_ad.ad.final_urls
        FROM ad_group_ad
        WHERE campaign.name = 'Google-Sa-CP-TW' 
          AND ad_group.status = 'ENABLED' 
          AND ad_group_ad.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ads)
    ops = []
    
    for batch in stream:
        for row in batch.results:
            if 'postman' in row.ad_group.name.lower():
                print(f"Current URLs: {row.ad_group_ad.ad.final_urls}")
                op = client.get_type('AdOperation')
                ad = op.update
                ad.resource_name = ad_service.ad_path(CUSTOMER_ID, row.ad_group_ad.ad.id)
                # Overwrite final URLs list with just the new TW URL
                ad.final_urls.append(NEW_TW_URL)
                op.update_mask.paths.append("final_urls")
                ops.append(op)
            
    if ops:
        print(f"Updating Final URLs for {len(ops)} ads via AdService...")
        req = client.get_type('MutateAdsRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ops)
        req.partial_failure = True
        resp = ad_service.mutate_ads(request=req)
        if resp.partial_failure_error and resp.partial_failure_error.details:
            for err in resp.partial_failure_error.details:
                print(f"Error: {err}")
        else:
            print(f"Taiwan Landing URLs updated successfully.")
            
    print("[SUCCESS] All Active TW RSAs URLs Updated via AdService!")

if __name__ == '__main__':
    update_tw_url()
