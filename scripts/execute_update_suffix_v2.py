import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'
NEW_SUFFIX = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

def update_suffix():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    ad_service = client.get_service('AdService')
    
    q_ads = """
        SELECT ad_group_ad.ad.id, ad_group.id, campaign.name, ad_group.name, ad_group_ad.ad.final_url_suffix
        FROM ad_group_ad
        WHERE campaign.name LIKE '%Google-Sa-CP-%' 
          AND ad_group.status = 'ENABLED' 
          AND ad_group_ad.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ads)
    ops = []
    
    for batch in stream:
        for row in batch.results:
            if 'postman' in row.ad_group.name.lower():
                print(f"Current Suffix: {row.ad_group_ad.ad.final_url_suffix}")
                op = client.get_type('AdOperation')
                ad = op.update
                # Resource name for Ad is customers/{customer_id}/ads/{ad_id}
                ad.resource_name = ad_service.ad_path(CUSTOMER_ID, row.ad_group_ad.ad.id)
                ad.final_url_suffix = NEW_SUFFIX
                op.update_mask.paths.append("final_url_suffix")
                ops.append(op)
            
    if ops:
        print(f"Updating URL Suffix for {len(ops)} ads via AdService...")
        for i in range(0, len(ops), 100):
            req = client.get_type('MutateAdsRequest')
            req.customer_id = CUSTOMER_ID
            req.operations.extend(ops[i:i+100])
            req.partial_failure = True
            resp = ad_service.mutate_ads(request=req)
            if resp.partial_failure_error and resp.partial_failure_error.details:
                for err in resp.partial_failure_error.details:
                    print(f"Error: {err}")
            else:
                print(f"Batch updated successfully.")
            
    print("[SUCCESS] All Active RSAs URL Suffixes Updated via AdService!")

if __name__ == '__main__':
    update_suffix()
