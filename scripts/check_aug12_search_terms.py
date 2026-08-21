import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

TARGETS = [
    "Google-Sa-Mintlify-Global",
    "Google-Sa-Jmeter-Global",
    "Google-Sa-Category-Competitor-Global"
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
        WHERE campaign.name IN ({', '.join([f"'{c}'" for c in TARGETS])})
          AND segments.date = '2026-08-12'
          AND metrics.cost_micros > 1000000
        ORDER BY metrics.cost_micros DESC
    """
    
    print("=== AUG 12 HIGH COST SEARCH TERMS ===")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            cname = row.campaign.name
            st = row.search_term_view.search_term
            cost = row.metrics.cost_micros / 1000000.0
            clicks = row.metrics.clicks
            conv = row.metrics.conversions
            try:
                print(f"[{cname:<35}] Term: '{st:<35}' | Spend: ${cost:<5.2f} | Clicks: {clicks} | Convs: {conv:.1f}")
            except:
                pass

if __name__ == '__main__':
    main()
