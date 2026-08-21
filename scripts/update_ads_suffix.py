import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
ad_group_ad_service = client.get_service("AdGroupAdService")
customer_id = '9496728294'

ad_groups_to_update = ['API-Docs-Generation', 'Mock-Server-Frontend', 'Testing-Multi-Protocol']
suffix_str = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

q = f"""
    SELECT ad_group_ad.ad.id, ad_group.id, ad_group_ad.ad.final_url_suffix, ad_group_ad.ad.tracking_url_template
    FROM ad_group_ad
    WHERE ad_group.name IN ('API-Docs-Generation', 'Mock-Server-Frontend', 'Testing-Multi-Protocol')
"""

stream = ga_service.search_stream(customer_id=customer_id, query=q)
ops = []

for batch in stream:
    for row in batch.results:
        op = client.get_type('AdGroupAdOperation')
        ad = op.update
        # The resource name requires customer_id, ad_group_id, and ad_id
        ad.resource_name = ad_group_ad_service.ad_group_ad_path(customer_id, row.ad_group.id, row.ad_group_ad.ad.id)
        
        ad.ad.final_url_suffix = suffix_str
        op.update_mask.paths.append("ad.final_url_suffix")
        
        # Clear tracking_url_template to avoid duplication
        ad.ad.tracking_url_template = ""
        op.update_mask.paths.append("ad.tracking_url_template")
        
        ops.append(op)

if ops:
    try:
        resp = ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=ops)
        print(f"Successfully updated {len(resp.results)} ads with Final URL suffix.")
    except Exception as e:
        print(f"Error updating ads: {e}")
else:
    print("No ads found to update.")
