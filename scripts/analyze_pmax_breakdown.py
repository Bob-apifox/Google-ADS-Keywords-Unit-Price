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
    print("[DEEP PMAX ANALYSIS: NETWORK, CONVERSION ACTIONS, ASSET GROUPS]")
    print("==========================================================================")

    # 1. Conversion Action breakdown for PMax
    q_conv = """
        SELECT
            campaign.name,
            conversion_action.name,
            conversion_action.category,
            metrics.conversions,
            metrics.all_conversions
        FROM campaign
        WHERE campaign.name IN ('Google-PMax-CP-Global', 'Google-PMax-Postman')
          AND segments.date = '2026-08-11'
    """
    print("\n--- 1. [Conversion Actions Triggered on Aug 11] ---")
    try:
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_conv):
            for row in batch.results:
                cname = row.campaign.name
                ca_name = row.conversion_action.name
                cat = row.conversion_action.category.name
                conv = row.metrics.conversions
                all_conv = row.metrics.all_conversions
                print(f"[{cname}] Action: {ca_name:<35} | Cat: {cat:<15} | Convs: {conv:<6.1f} | All Convs: {all_conv:<6.1f}")
    except Exception as e:
        print(f"Error querying conversion actions: {e}")

    # 2. Asset Group performance on Aug 11
    q_ag = """
        SELECT
            campaign.name,
            asset_group.id,
            asset_group.name,
            asset_group.status,
            asset_group.final_urls,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions
        FROM asset_group
        WHERE campaign.name IN ('Google-PMax-CP-Global', 'Google-PMax-Postman')
          AND segments.date = '2026-08-11'
    """
    print("\n--- 2. [Asset Group Performance on Aug 11] ---")
    try:
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
            for row in batch.results:
                cname = row.campaign.name
                ag_name = row.asset_group.name
                cost = row.metrics.cost_micros / 1000000.0
                clicks = row.metrics.clicks
                impr = row.metrics.impressions
                conv = row.metrics.conversions
                url = row.asset_group.final_urls[0] if row.asset_group.final_urls else "N/A"
                print(f"[{cname}] Group: {ag_name:<30} | Cost: ${cost:<6.2f} | Clicks: {clicks:<4} | Impr: {impr:<5} | Convs: {conv:<6.1f} | Final URL: {url}")
    except Exception as e:
        print(f"Error querying asset groups: {e}")

    # 3. Geo breakdown for PMax on Aug 11
    q_geo = """
        SELECT
            campaign.name,
            campaign.advertising_channel_type,
            geographic_view.country_criterion_id,
            metrics.cost_micros,
            metrics.clicks,
            metrics.conversions
        FROM geographic_view
        WHERE campaign.name IN ('Google-PMax-CP-Global', 'Google-PMax-Postman')
          AND segments.date = '2026-08-11'
          AND metrics.cost_micros > 500000
    """
    print("\n--- 3. [Top Geos for PMax on Aug 11] ---")
    try:
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_geo):
            for row in batch.results:
                cname = row.campaign.name
                cid = row.geographic_view.country_criterion_id
                cost = row.metrics.cost_micros / 1000000.0
                clicks = row.metrics.clicks
                conv = row.metrics.conversions
                print(f"[{cname}] Country ID: {cid:<10} | Cost: ${cost:<6.2f} | Clicks: {clicks:<4} | Convs: {conv:<6.1f}")
    except Exception as e:
        print(f"Error querying geo: {e}")

if __name__ == '__main__':
    main()
