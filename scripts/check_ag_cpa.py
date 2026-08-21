import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')

q = "SELECT ad_group.name, ad_group.target_cpa_micros, campaign.maximize_conversions.target_cpa_micros FROM ad_group WHERE campaign.name = 'Google-Sa-DSA-Global'"
for batch in ga_service.search_stream(customer_id='9496728294', query=q):
    for row in batch.results:
        camp_cpa = row.campaign.maximize_conversions.target_cpa_micros
        ag_cpa = row.ad_group.target_cpa_micros
        print(f"AdGroup: {row.ad_group.name} | Campaign CPA: {camp_cpa} | AdGroup CPA: {ag_cpa}")
