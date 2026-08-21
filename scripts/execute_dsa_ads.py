import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

ADS_CONFIG = {
    'DSA-Group-Postman-Alt-Blogs': {
        'desc1': 'Migrate from Postman to Apidog seamlessly. Import all data with zero loss.',
        'desc2': 'Free, powerful API design, debugging, and testing tool for your entire team.'
    },
    'DSA-Group-Enterprise-Tech': {
        'desc1': 'Advanced API testing and documentation for SOAP, WebSocket, and REST.',
        'desc2': 'Enterprise-grade security, CI/CD integration, and unlimited collaboration.'
    }
}

def execute_dsa_ads():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    ag_ad_service = client.get_service('AdGroupAdService')
    
    # Get AdGroup Resource Names
    q = "SELECT ad_group.name, ad_group.resource_name FROM ad_group WHERE ad_group.name IN ('DSA-Group-Postman-Alt-Blogs', 'DSA-Group-Enterprise-Tech') AND ad_group.status = 'ENABLED'"
    ag_map = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            ag_map[row.ad_group.name] = row.ad_group.resource_name
            
    ops = []
    for ag_name, ad_texts in ADS_CONFIG.items():
        if ag_name not in ag_map:
            print(f"Could not find AdGroup: {ag_name}")
            continue
            
        op = client.get_type("AdGroupAdOperation")
        ad_group_ad = op.create
        ad_group_ad.ad_group = ag_map[ag_name]
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        ad = ad_group_ad.ad
        ad.expanded_dynamic_search_ad.description = ad_texts['desc1']
        ad.expanded_dynamic_search_ad.description2 = ad_texts['desc2']
        ops.append(op)
        
    if ops:
        print(f"Creating {len(ops)} Expanded Dynamic Search Ads...")
        req = client.get_type("MutateAdGroupAdsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ops)
        req.partial_failure = True
        resp = ag_ad_service.mutate_ad_group_ads(request=req)
        
        if resp.partial_failure_error and resp.partial_failure_error.details:
            for err in resp.partial_failure_error.details:
                print(f"Error creating ad: {err}")
        else:
            for res in resp.results:
                print(f"Created Ad: {res.resource_name}")
            print("[SUCCESS] DSA Ads created successfully!")
            
if __name__ == '__main__':
    execute_dsa_ads()
