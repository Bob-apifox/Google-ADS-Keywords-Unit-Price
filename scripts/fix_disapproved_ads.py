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
    
    # Query DISAPPROVED ads due to DESTINATION_NOT_WORKING
    query = """
        SELECT
            campaign.name,
            ad_group.name,
            ad_group_ad.resource_name,
            ad_group_ad.ad.id,
            ad_group_ad.ad.final_urls,
            ad_group_ad.policy_summary.approval_status
        FROM ad_group_ad
        WHERE ad_group_ad.policy_summary.approval_status = 'DISAPPROVED'
    """
    
    ops = []
    stream = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in stream:
        res_name = row.ad_group_ad.resource_name
        urls = list(row.ad_group_ad.ad.final_urls)
        cname = row.campaign.name
        agname = row.ad_group.name
        
        # Check if URL contains destination issue
        for entry in row.ad_group_ad.policy_summary.policy_topic_entries:
            if entry.topic == "DESTINATION_NOT_WORKING":
                print(f"Fixing DESTINATION_NOT_WORKING ad in '{cname} > {agname}' | Old URL: {urls}")
                op = client.get_type("AdGroupAdOperation")
                ad_group_ad = op.update
                ad_group_ad.resource_name = res_name
                ad_group_ad.ad.final_urls.append("https://apidog.com/")
                op.update_mask.paths.append("ad.final_urls")
                ops.append((cname, agname, op))
                break

    print(f"Prepared {len(ops)} operations to fix broken Final URLs.")
    
    if ops:
        req = client.get_type("MutateAdGroupAdsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend([item[2] for item in ops])
        req.partial_failure = True
        
        try:
            res = ad_group_ad_service.mutate_ad_group_ads(request=req)
            print(f"✅ Successfully updated {len(ops)} ads with valid working Final URLs!")
        except Exception as e:
            print(f"Error updating ad final URLs: {e}")

if __name__ == '__main__':
    main()
