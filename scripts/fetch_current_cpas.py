import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

def main():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        ga_service = client.get_service("GoogleAdsService")
        
        # We need to fetch campaign and ad group target CPAs
        # First, Campaign level
        query_camp = """
            SELECT campaign.id, campaign.name, campaign.target_cpa.target_cpa_micros, campaign.bidding_strategy_type
            FROM campaign
            WHERE campaign.status = 'ENABLED'
        """
        print("--- CAMPAIGN TARGET CPAs ---")
        stream_camp = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_camp)
        for batch in stream_camp:
            for row in batch.results:
                cpa_micros = row.campaign.target_cpa.target_cpa_micros
                cpa = cpa_micros / 1000000 if cpa_micros else 'Not Set'
                print(f"Camp: {row.campaign.name} (ID: {row.campaign.id}) - Target CPA: {cpa}")

        print("\\n--- AD GROUP TARGET CPAs (for high spenders) ---")
        query_ag = """
            SELECT campaign.name, ad_group.id, ad_group.name, ad_group.target_cpa_micros, ad_group.status
            FROM ad_group
            WHERE ad_group.status = 'ENABLED'
        """
        stream_ag = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_ag)
        for batch in stream_ag:
            for row in batch.results:
                cpa_micros = row.ad_group.target_cpa_micros
                cpa = cpa_micros / 1000000 if cpa_micros else 'Inherited'
                if row.campaign.name in ['Google-Sa-Comp-VSCode-Global', 'Google-Sa-Design-Global', 'Google-Sa-SpecFirst-Global', 'Google-Sa-API Editor-Global', 'Google-Sa-CP-Global', 'Google-Sa-Scalar-Global', 'Google-Sa-Expansion-Horizon-2026', 'Google-Sa-Bump.sh-Global']:
                    print(f"[{row.campaign.name}] AG: {row.ad_group.name} (ID: {row.ad_group.id}) - Target CPA: {cpa}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
