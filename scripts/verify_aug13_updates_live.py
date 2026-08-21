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
            campaign.name,
            campaign_budget.amount_micros,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros
        FROM campaign
        WHERE campaign.name IN (
            'Google-Sa-Mintlify-Global',
            'Google-Sa-Jmeter-Global',
            'Google-Sa-Category-Competitor-Global',
            'Google-PMax-CP-Global'
        )
    """
    print("=== LIVE VERIFICATION OF 8.13 BUDGET UPDATES ===")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            c = row.campaign
            b = row.campaign_budget.amount_micros / 1000000.0
            tcpa = (c.maximize_conversions.target_cpa_micros or c.target_cpa.target_cpa_micros) / 1000000.0 if (c.maximize_conversions.target_cpa_micros or c.target_cpa.target_cpa_micros) else 0.0
            print(f"[{c.name:<38}] Live Budget: ${b:<6.2f}/day | Live Target CPA: ${tcpa:.2f}")

if __name__ == '__main__':
    main()
