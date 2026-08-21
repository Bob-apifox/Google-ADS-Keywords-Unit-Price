import os
import sys
import urllib3
from google.ads.googleads.client import GoogleAdsClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ["GOOGLE_ADS_USE_REST"] = "true"
sys.stdout.reconfigure(encoding='utf-8')

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_ad_service = client.get_service("AdGroupAdService")
    
    query = """
        SELECT
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group.resource_name,
            ad_group_ad.resource_name,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.ad.responsive_search_ad.descriptions,
            ad_group_ad.policy_summary.approval_status,
            ad_group_ad.policy_summary.policy_topic_entries
        FROM ad_group_ad
        WHERE ad_group_ad.policy_summary.approval_status = 'DISAPPROVED'
    """
    
    pause_ops = []
    create_ops = []
    
    stream = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in stream:
        res_name = row.ad_group_ad.resource_name
        ag_res = row.ad_group.resource_name
        cname = row.campaign.name
        agname = row.ad_group.name
        
        is_dest_error = False
        for entry in row.ad_group_ad.policy_summary.policy_topic_entries:
            if entry.topic == "DESTINATION_NOT_WORKING":
                is_dest_error = True
                break
                
        if is_dest_error:
            # 1. Pause old disapproved ad
            op_pause = client.get_type("AdGroupAdOperation")
            ad_pause = op_pause.update
            ad_pause.resource_name = res_name
            ad_pause.status = client.enums.AdGroupAdStatusEnum.PAUSED
            op_pause.update_mask.paths.append("status")
            pause_ops.append(op_pause)
            
            # 2. Create new RSA ad with valid working final URL
            op_create = client.get_type("AdGroupAdOperation")
            ad_create = op_create.create
            ad_create.ad_group = ag_res
            ad_create.status = client.enums.AdGroupAdStatusEnum.ENABLED
            ad_create.ad.final_urls.append("https://apidog.com/")
            
            # Copy headlines and descriptions
            for h in row.ad_group_ad.ad.responsive_search_ad.headlines:
                head = client.get_type("AdTextAsset")
                head.text = h.text
                ad_create.ad.responsive_search_ad.headlines.append(head)
                
            for d in row.ad_group_ad.ad.responsive_search_ad.descriptions:
                desc = client.get_type("AdTextAsset")
                desc.text = d.text
                ad_create.ad.responsive_search_ad.descriptions.append(desc)
                
            create_ops.append(op_create)
            print(f"Prepared fix for DISAPPROVED ad in '{cname} > {agname}'")

    print(f"Pause Ops: {len(pause_ops)} | Create Ops: {len(create_ops)}")
    
    if pause_ops:
        req = client.get_type("MutateAdGroupAdsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(pause_ops)
        req.partial_failure = True
        ad_group_ad_service.mutate_ad_group_ads(request=req)
        print("✅ Paused old disapproved ads with broken URLs!")
        
    if create_ops:
        req = client.get_type("MutateAdGroupAdsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(create_ops)
        req.partial_failure = True
        ad_group_ad_service.mutate_ad_group_ads(request=req)
        print("✅ Created new compliant RSA ads with valid working Final URLs (https://apidog.com/)!")

if __name__ == '__main__':
    main()
