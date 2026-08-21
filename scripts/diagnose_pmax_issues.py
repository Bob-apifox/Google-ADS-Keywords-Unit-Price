import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    print("==========================================================================")
    print("[DEEP DIAGNOSIS: PMAX PERFORMANCE ISSUES ON 2026-08-11]")
    print("==========================================================================")

    # 1. Device Breakdown for PMax on Aug 11
    q_device = """
        SELECT
            campaign.name,
            segments.device,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions
        FROM campaign
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
          AND segments.date = '2026-08-11'
    """
    print("\n--- 1. [PMax Device Breakdown on Aug 11] ---")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_device):
        for row in batch.results:
            c = row.metrics.cost_micros / 1000000.0
            conv = row.metrics.conversions
            cpa = c / conv if conv > 0 else 0.0
            print(f"[{row.campaign.name}] Device: {row.segments.device.name:<10} | Cost: ${c:<6.2f} | Clicks: {row.metrics.clicks:<4} | Impr: {row.metrics.impressions:<5} | Convs: {conv:.1f} | Ads CPA: ${cpa:.2f}")

    # 2. Geo/Location Performance for PMax on Aug 11
    q_geo = """
        SELECT
            campaign.name,
            geographic_view.country_criterion_id,
            geographic_view.location_type,
            metrics.cost_micros,
            metrics.clicks,
            metrics.conversions
        FROM geographic_view
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
          AND segments.date = '2026-08-11'
          AND metrics.cost_micros > 500000
    """
    print("\n--- 2. [PMax Top Country Cost Breakdown on Aug 11] ---")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_geo):
        for row in batch.results:
            c = row.metrics.cost_micros / 1000000.0
            conv = row.metrics.conversions
            cpa = c / conv if conv > 0 else 0.0
            print(f"[{row.campaign.name}] Country ID: {row.geographic_view.country_criterion_id} | Cost: ${c:<6.2f} | Clicks: {row.metrics.clicks} | Convs: {conv:.1f}")

    # 3. Search Category Insights for PMax (Last 7 Days vs Aug 11)
    q_search_cat = """
        SELECT
            campaign.name,
            campaign_search_term_insight.category_label,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions
        FROM campaign_search_term_insight
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
          AND segments.date = '2026-08-11'
    """
    print("\n--- 3. [PMax Search Term Insights on Aug 11] ---")
    found_cat = 0
    try:
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_search_cat):
            for row in batch.results:
                found_cat += 1
                cat = row.campaign_search_term_insight.category_label
                print(f"[{row.campaign.name}] Search Category: {cat:<30} | Clicks: {row.metrics.clicks:<4} | Impr: {row.metrics.impressions:<5} | Convs: {row.metrics.conversions:.1f}")
    except Exception as e:
        print(f"Note on search term insight: {e}")

if __name__ == '__main__':
    main()
