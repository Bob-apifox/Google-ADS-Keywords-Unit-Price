import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def verify_live():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    
    q = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign_budget.amount_micros,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros
        FROM campaign
        WHERE campaign.status != 'REMOVED'
        ORDER BY campaign.status, campaign.name
    """
    print(f"\n{'Campaign Name':<38} | {'Type':<8} | {'Status':<7} | {'Budget/Day':<10} | {'Target CPA'}")
    print("="*85)
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            cname = row.campaign.name
            ctype = row.campaign.advertising_channel_type.name
            cstatus = row.campaign.status.name
            b_micros = row.campaign_budget.amount_micros
            budget_str = f"${b_micros/1000000.0:.2f}" if b_micros else "$0.00"
            
            tcpa_micros = row.campaign.maximize_conversions.target_cpa_micros or row.campaign.target_cpa.target_cpa_micros
            tcpa_str = f"${tcpa_micros/1000000.0:.2f}" if tcpa_micros else "Auto Max"
            
            if cstatus == 'ENABLED':
                print(f"{cname:<38} | {ctype:<8} | {cstatus:<7} | {budget_str:<10} | {tcpa_str}")

if __name__ == '__main__':
    verify_live()
