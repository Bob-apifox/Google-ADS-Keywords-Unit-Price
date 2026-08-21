import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
customer_id = '9496728294'
campaign_id = '21982653330'

query = f"""
    SELECT campaign_criterion.location.geo_target_constant
    FROM campaign_criterion
    WHERE campaign.id = {campaign_id}
    AND campaign_criterion.negative = TRUE
    AND campaign_criterion.type = 'LOCATION'
"""

stream = ga_service.search_stream(customer_id=customer_id, query=query)
print("Negative Locations for Google-Sa-Postman-Global:")
for batch in stream:
    for row in batch.results:
        print(f"ID: {row.campaign_criterion.location.geo_target_constant}")
