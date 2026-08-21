import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

try:
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    print("--- CPA Checks ---")
    def get_cpa(campaign_name):
        query = f"SELECT campaign.name, campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros, ad_group.name, ad_group.target_cpa_micros FROM ad_group WHERE campaign.name = '{campaign_name}' AND ad_group.status = 'ENABLED'"
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                camp_cpa = row.campaign.target_cpa.target_cpa_micros
                ag_cpa = row.ad_group.target_cpa_micros
                b_type = row.campaign.bidding_strategy_type.name
                print(f"Camp: {campaign_name} | Strategy: {b_type} | Camp CPA: ${camp_cpa/1e6 if camp_cpa else 'N/A'} | AG: {row.ad_group.name} | AG CPA: ${ag_cpa/1e6 if ag_cpa else 'N/A'}")

    for c in ['Google-Sa-Fern-Global', 'Google-Sa-Debug-Global', 'Google-Sa-Readme-Global']:
        get_cpa(c)
        
    print("\n--- KW Checks ---")
    def get_kws(campaign_name):
        query = f"SELECT ad_group.name, ad_group.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.conversions, metrics.cost_micros FROM keyword_view WHERE campaign.name = '{campaign_name}' AND segments.date DURING LAST_30_DAYS AND metrics.conversions > 9"
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                cost = row.metrics.cost_micros / 1e6
                convs = row.metrics.conversions
                cpa = cost / convs if convs > 0 else 0
                if cpa < 3.5 and row.ad_group_criterion.keyword.match_type.name != 'BROAD':
                    print(f"Camp: {campaign_name} | AG: {row.ad_group.name} | KW: {row.ad_group_criterion.keyword.text} | Match: {row.ad_group_criterion.keyword.match_type.name} | Convs: {convs} | CPA: ${cpa:.2f}")

    for c in ['Google-Sa-Postman-Global', 'Google-Sa-Openapi-Global', 'Google-Sa-CP-Global']:
        get_kws(c)
except Exception as e:
    print(f"Error: {e}")
