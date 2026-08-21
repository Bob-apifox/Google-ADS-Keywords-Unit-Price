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

    q = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_budget.amount_micros,
            campaign.target_cpa.target_cpa_micros,
            campaign.maximize_conversions.target_cpa_micros
        FROM campaign
        WHERE campaign.id = 21976077538
    """
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            c = row.campaign
            b = row.campaign_budget.amount_micros / 1000000.0
            print(f"Campaign: {c.name} | Budget: ${b}/day | Status: {c.status.name}")

    q_ag = """
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.status,
            ad_group.optimized_targeting_enabled
        FROM ad_group
        WHERE campaign.id = 21976077538
    """
    print("\nAd Groups:")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
        for row in batch.results:
            ag = row.ad_group
            print(f"  Ad Group: {ag.name} (ID: {ag.id}, Status: {ag.status.name}, Optimized Targeting: {ag.optimized_targeting_enabled})")

if __name__ == '__main__':
    main()
