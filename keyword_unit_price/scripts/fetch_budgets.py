import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

target_campaigns = [
    "Google-Sa-CP-Global",
    "Google-Sa-Fern-Global",
    "Google-Sa-DSA-Postman-Global",
    "Google-Sa-Category-Competitor-Global"
]

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")

query = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.campaign_budget,
        campaign_budget.amount_micros,
        campaign_budget.id
    FROM campaign
    WHERE campaign.status = 'ENABLED'
"""

stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
for batch in stream:
    for row in batch.results:
        if row.campaign.name in target_campaigns:
            print(f"Campaign: {row.campaign.name}")
            print(f"Budget ID: {row.campaign_budget.id}")
            print(f"Current Budget: {row.campaign_budget.amount_micros / 1000000.0} USD")
            print("---")
