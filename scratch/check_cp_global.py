import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
customer_id = '9496728294'

query = """
    SELECT
        campaign.name,
        campaign.id,
        campaign.status,
        campaign.bidding_strategy_type,
        campaign.target_cpa.target_cpa_micros,
        campaign_budget.amount_micros,
        metrics.cost_micros,
        metrics.clicks,
        metrics.impressions,
        metrics.conversions,
        segments.date
    FROM campaign
    WHERE campaign.name = 'Google-Sa-CP-Global'
    AND segments.date DURING LAST_7_DAYS
    ORDER BY segments.date DESC
"""

response = ga_service.search(customer_id=customer_id, query=query)
print("Data for Google-Sa-CP-Global:")
for row in response:
    date = row.segments.date
    cost = row.metrics.cost_micros / 1e6
    clicks = row.metrics.clicks
    imps = row.metrics.impressions
    conv = row.metrics.conversions
    tcpa = row.campaign.target_cpa.target_cpa_micros / 1e6 if row.campaign.target_cpa.target_cpa_micros else 0
    budget = row.campaign_budget.amount_micros / 1e6
    print(f"Date: {date} | Budget: ${budget} | tCPA: ${tcpa} | Cost: ${cost:.2f} | Clicks: {clicks} | Imps: {imps} | Convs: {conv}")
