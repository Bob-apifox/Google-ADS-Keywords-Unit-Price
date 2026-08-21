import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
campaign_service = client.get_service('CampaignService')
customer_id = '9496728294'

campaign_names = ['Google-Sa-Swagger-Global', 'Google-Sa-Mock-Global', 'Google-Sa-Testing-Global']
suffix_str = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

q = """
    SELECT campaign.id, campaign.name, campaign.tracking_url_template, campaign.url_custom_parameters, campaign.final_url_suffix
    FROM campaign 
    WHERE campaign.name IN ('Google-Sa-Swagger-Global', 'Google-Sa-Mock-Global', 'Google-Sa-Testing-Global')
"""

stream = ga_service.search_stream(customer_id=customer_id, query=q)
ops = []

for batch in stream:
    for row in batch.results:
        print(f"Updating Campaign: {row.campaign.name}")
        op = client.get_type('CampaignOperation')
        campaign = op.update
        campaign.resource_name = campaign_service.campaign_path(customer_id, row.campaign.id)
        
        # In the Google Ads API, tracking templates and suffixes should typically be set at the Campaign or AdGroup level.
        # AD level tracking template is immutable after creation.
        campaign.tracking_url_template = "{lpurl}"
        campaign.final_url_suffix = suffix_str
        
        op.update_mask.paths.append("tracking_url_template")
        op.update_mask.paths.append("final_url_suffix")
        ops.append(op)

if ops:
    try:
        resp = campaign_service.mutate_campaigns(customer_id=customer_id, operations=ops)
        print(f"Successfully updated {len(resp.results)} campaigns with Final URL suffix at the Campaign level.")
    except Exception as e:
        print(f"Error updating campaigns: {e}")
