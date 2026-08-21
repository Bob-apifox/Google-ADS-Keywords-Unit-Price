import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

client = GoogleAdsClient.load_from_storage("common/config/google-ads.yaml")
ga_service = client.get_service("GoogleAdsService")
query = """
    SELECT campaign.name, ad_group.name, ad_group.id
    FROM ad_group
    WHERE campaign.name IN ('Google-Sa-Solutions-API-First-Global', 'Google-Sa-DSA-Postman-Global')
      AND ad_group.status = 'ENABLED'
"""
stream = ga_service.search_stream(customer_id="9496728294", query=query)
for batch in stream:
    for row in batch.results:
        print(f"[{row.campaign.name}] -> [{row.ad_group.name}] (ID: {row.ad_group.id})")
