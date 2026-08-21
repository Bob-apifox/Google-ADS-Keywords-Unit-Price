import os
import sys
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")

target_camps = [
    "Google-Sa-Comp-HeavyQA-Global",
    "Google-Sa-Fern-Global",
    "Google-Sa-Comp-VSCode-Global",
    "Google-Sa-Design-Global",
    "Google-Sa-Expansion-Horizon-2026",
    "Google-Sa-Testing-Global"
]

for c_name in target_camps:
    query = f"""
        SELECT
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group.status
        FROM ad_group
        WHERE campaign.name = '{c_name}'
          AND ad_group.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    print(f"=== {c_name} Ad Groups ===")
    for batch in stream:
        for row in batch.results:
            print(f"  - [{row.ad_group.id}] {row.ad_group.name}")
