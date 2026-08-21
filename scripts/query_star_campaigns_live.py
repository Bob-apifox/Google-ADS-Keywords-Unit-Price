import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

STAR_CAMPAIGNS = [
    "Google-Sa-Jmeter-Global",
    "Google-Sa-Readme-Global",
    "Google-Sa-Hoppscotch-Global",
    "Google-Sa-API Editor-Global",
    "Google-Sa-Fern-Global",
    "Google-Sa-Func-MultiProtocol-Global",
    "Google-Sa-Bruno-Global"
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_budget.amount_micros,
            campaign.bidding_strategy_type,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros
        FROM campaign
        WHERE campaign.name IN ({', '.join([f"'{c}'" for c in STAR_CAMPAIGNS])})
    """
    
    print("=== LIVE CURRENT SETTINGS IN GOOGLE ADS ===")
    print(f"{'Campaign Name':<36} | {'ID':<12} | {'Current Budget':<15} | {'Bidding Strategy':<22} | {'Current Target CPA'}")
    print("-" * 115)
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            c = row.campaign
            b_usd = row.campaign_budget.amount_micros / 1000000.0
            
            tcpa = "None (Max Conv)"
            if c.maximize_conversions.target_cpa_micros > 0:
                tcpa = f"${c.maximize_conversions.target_cpa_micros / 1000000.0:.2f}"
            elif c.target_cpa.target_cpa_micros > 0:
                tcpa = f"${c.target_cpa.target_cpa_micros / 1000000.0:.2f}"
                
            print(f"{c.name:<36} | {c.id:<12} | ${b_usd:<14.2f} | {c.bidding_strategy_type.name:<22} | {tcpa}")

if __name__ == '__main__':
    main()
