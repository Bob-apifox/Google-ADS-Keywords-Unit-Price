import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga = client.get_service('GoogleAdsService')

q = "SELECT campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros FROM campaign WHERE campaign.name = 'Google-Sa-DSA-Global'"
for batch in ga.search_stream(customer_id='9496728294', query=q):
    for row in batch.results:
        print(f"Type: {row.campaign.bidding_strategy_type.name}")
        if row.campaign.target_cpa:
            print(f"Target CPA: {row.campaign.target_cpa.target_cpa_micros}")
