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

    # 1. Performance Max Placements
    q_place = """
        SELECT
            campaign.name,
            performance_max_placement_view.placement,
            performance_max_placement_view.placement_type,
            performance_max_placement_view.target_url,
            metrics.impressions
        FROM performance_max_placement_view
        WHERE campaign.name IN ('Google-PMax-CP-Global', 'Google-PMax-Postman')
          AND segments.date = '2026-08-11'
        ORDER BY metrics.impressions DESC
        LIMIT 30
    """
    print("=== TOP 30 PMAX PLACEMENTS ON AUG 11 ===")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_place):
        for row in batch.results:
            cname = row.campaign.name
            p = row.performance_max_placement_view.placement
            pt = row.performance_max_placement_view.placement_type.name
            impr = row.metrics.impressions
            print(f"[{cname}] Type: {pt:<20} | Impr: {impr:<6} | Placement: {p}")

    # 2. Check Geo Target Settings of PMax
    q_loc = """
        SELECT
            campaign.name,
            campaign_criterion.location.geo_target_constant,
            campaign_criterion.negative,
            campaign_criterion.status
        FROM campaign_criterion
        WHERE campaign.name IN ('Google-PMax-CP-Global', 'Google-PMax-Postman')
          AND campaign_criterion.type = 'LOCATION'
    """
    print("\n=== PMAX GEO LOCATION CRITERIA ===")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_loc):
        for row in batch.results:
            cname = row.campaign.name
            loc = row.campaign_criterion.location.geo_target_constant
            neg = row.campaign_criterion.negative
            print(f"[{cname}] Geo Target: {loc} | Negative: {neg} | Status: {row.campaign_criterion.status.name}")

if __name__ == '__main__':
    main()
