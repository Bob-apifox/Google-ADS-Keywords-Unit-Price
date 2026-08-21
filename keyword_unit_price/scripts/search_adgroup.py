import os
import sys
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")

# Search ad group with ID 188453907761
query_ag = """
    SELECT
        campaign.id,
        campaign.name,
        ad_group.id,
        ad_group.name,
        ad_group.status
    FROM ad_group
    WHERE ad_group.id = 188453907761
"""

stream_ag = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_ag)
found_ag = False
for batch in stream_ag:
    for row in batch.results:
        found_ag = True
        print(f"Found AdGroup! Campaign: {row.campaign.name} ({row.campaign.id}) | AdGroup: {row.ad_group.name} ({row.ad_group.id}) | Status: {row.ad_group.status}")

if not found_ag:
    print("AdGroup 188453907761 not found in account 9496728294.")

# Let's search all ad groups with 'Mintlify' in name
query_all_mint = """
    SELECT
        campaign.id,
        campaign.name,
        ad_group.id,
        ad_group.name,
        ad_group.status
    FROM ad_group
    WHERE ad_group.name LIKE '%Mintlify%'
"""
stream_mint = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_all_mint)
for batch in stream_mint:
    for row in batch.results:
        print(f"Mintlify AdGroup: Campaign {row.campaign.name} ({row.campaign.id}) | AdGroup {row.ad_group.name} ({row.ad_group.id}) | Status {row.ad_group.status}")
