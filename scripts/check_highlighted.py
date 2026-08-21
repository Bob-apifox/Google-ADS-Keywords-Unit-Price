import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

client = GoogleAdsClient.load_from_storage(r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml")
customer_id = "9496728294"

campaigns = [
    "Google-Sa-DSA-Global",
    "Google-Sa-Readme-Global",
    "Google-Sa-SpecFirst-Global",
    "Google-Sa-Expansion-Horizon-2026",
    "Google-Sa-Solutions-Multi-Protocol-Global",
    "Google-Sa-Solutions-Unified-API-Global",
    "Google-Sa-API Editor-Global"
]

ga_service = client.get_service("GoogleAdsService")

print(f"{'Campaign Name':<45} | {'Cost':<8} | {'Convs':<6} | {'CPA':<6} | {'Status'}")
print("-" * 80)

for name in campaigns:
    query = f"""
        SELECT campaign.status, metrics.cost_micros, metrics.conversions
        FROM campaign
        WHERE segments.date DURING LAST_7_DAYS
          AND campaign.name = '{name}'
    """
    try:
        response = ga_service.search(customer_id=customer_id, query=query)
        found = False
        for row in response:
            found = True
            cost = row.metrics.cost_micros / 1000000.0
            convs = row.metrics.conversions
            cpa = cost / convs if convs > 0 else 0
            status = row.campaign.status.name
            print(f"{name:<45} | ${cost:<7.2f} | {convs:<6} | ${cpa:<5.2f} | {status}")
        if not found:
            print(f"{name:<45} | Not found or 0 data")
    except Exception as e:
        print(f"Error fetching {name}: {e}")
