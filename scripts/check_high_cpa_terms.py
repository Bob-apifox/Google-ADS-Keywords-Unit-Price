import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

HIGH_CPA_CAMPAIGNS = [
    "Google-Sa-API Editor-Global",
    "Google-Sa-CLI-Terminal-Global",
    "Google-Sa-Mintlify-Global",
    "Google-Sa-Openapi-Global"
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    q = f"""
        SELECT
            campaign.name,
            search_term_view.search_term,
            metrics.cost_micros,
            metrics.clicks,
            metrics.conversions
        FROM search_term_view
        WHERE campaign.name IN ({', '.join([f"'{c}'" for c in HIGH_CPA_CAMPAIGNS])})
          AND segments.date = '2026-08-11'
          AND metrics.cost_micros > 500000
        ORDER BY metrics.cost_micros DESC
    """
    
    print("=== SEARCH TERMS FOR HIGH CPA CAMPAIGNS ON AUG 11 ===")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            cname = row.campaign.name
            st = row.search_term_view.search_term
            cost = row.metrics.cost_micros / 1000000.0
            clicks = row.metrics.clicks
            conv = row.metrics.conversions
            print(f"[{cname:<30}] Search Term: '{st:<35}' | Cost: ${cost:<5.2f} | Clicks: {clicks} | Convs: {conv:.1f}")

if __name__ == '__main__':
    main()
