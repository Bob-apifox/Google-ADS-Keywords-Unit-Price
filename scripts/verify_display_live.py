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
            campaign.maximize_conversions.target_cpa_micros
        FROM campaign
        WHERE campaign.id IN (22341978472, 24185799797, 24185800049)
    """
    print("=== LIVE VERIFICATION OF PMAX & NEW DISPLAY CAMPAIGNS ===")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            c = row.campaign
            b = row.campaign_budget.amount_micros / 1000000.0
            tcpa = (c.maximize_conversions.target_cpa_micros or 0) / 1000000.0
            print(f"[{c.name:<35}] ID: {c.id} | Status: {c.status.name:<8} | Budget: ${b:<5.2f}/day | tCPA: ${tcpa:.2f}")

if __name__ == '__main__':
    main()
