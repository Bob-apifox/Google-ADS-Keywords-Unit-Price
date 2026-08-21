import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")

query = """
    SELECT
        segments.date,
        metrics.clicks,
        metrics.impressions,
        metrics.cost_micros,
        metrics.conversions
    FROM customer
    WHERE segments.date BETWEEN '2026-08-10' AND '2026-08-19'
    ORDER BY segments.date DESC
"""

stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
print(f"{'Date':<12} | {'Cost (USD)':<12} | {'Clicks':<8} | {'Impressions':<12} | {'Avg CPC':<10} | {'CTR':<8}")
print("-" * 75)
for batch in stream:
    for row in batch.results:
        d = row.segments.date
        cost = row.metrics.cost_micros / 1e6
        clicks = row.metrics.clicks
        impr = row.metrics.impressions
        cpc = cost / clicks if clicks > 0 else 0
        ctr = (clicks / impr * 100) if impr > 0 else 0
        print(f"{d:<12} | ${cost:<11.2f} | {clicks:<8} | {impr:<12} | ${cpc:<9.2f} | {ctr:<7.2f}%")
