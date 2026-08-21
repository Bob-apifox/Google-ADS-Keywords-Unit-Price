import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
budget_service = client.get_service('CampaignBudgetService')
customer_id = '9496728294'

def update_mock_budget():
    q = "SELECT campaign.id, campaign.name, campaign.campaign_budget FROM campaign WHERE campaign.name = 'Google-Sa-Mock-Global' AND campaign.status = 'ENABLED'"
    stream = ga_service.search_stream(customer_id=customer_id, query=q)
    for batch in stream:
        for row in batch.results:
            b_id = row.campaign.campaign_budget.split('/')[-1]
            op = client.get_type('CampaignBudgetOperation')
            budget = op.update
            budget.resource_name = budget_service.campaign_budget_path(customer_id, b_id)
            budget.amount_micros = 40000000  # $40
            op.update_mask.paths.append("amount_micros")
            
            resp = budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[op])
            print(f">>> Successfully updated Mock campaign budget to $40.00")
            return

def analyze_swagger():
    print("\n>>> Analyzing Google-Sa-Swagger-Global ...")
    # Get impression share and CPA for ad groups
    q_ag = """
        SELECT ad_group.name, ad_group.cpc_bid_micros, ad_group.target_cpa_micros,
               metrics.search_impression_share, metrics.cost_micros, metrics.conversions, metrics.impressions
        FROM ad_group
        WHERE campaign.name = 'Google-Sa-Swagger-Global' AND ad_group.status = 'ENABLED'
          AND segments.date DURING LAST_14_DAYS
    """
    try:
        stream = ga_service.search_stream(customer_id=customer_id, query=q_ag)
        for batch in stream:
            for row in batch.results:
                name = row.ad_group.name
                cpc = row.ad_group.cpc_bid_micros / 1000000 if row.ad_group.cpc_bid_micros else "N/A"
                tcpa = row.ad_group.target_cpa_micros / 1000000 if row.ad_group.target_cpa_micros else "N/A"
                imp_share = row.metrics.search_impression_share
                impr = row.metrics.impressions
                print(f"AdGroup: {name} | Impressions: {impr} | Search Imp Share: {imp_share} | CPC Limit: {cpc} | tCPA: {tcpa}")
    except Exception as e:
        print(f"Error querying ad groups: {e}")

    # Get keyword level issues (quality score, search volume)
    q_kw = """
        SELECT ad_group_criterion.keyword.text, ad_group.name, metrics.impressions, 
               metrics.search_impression_share, ad_group_criterion.quality_info.quality_score,
               ad_group_criterion.cpc_bid_micros
        FROM keyword_view
        WHERE campaign.name = 'Google-Sa-Swagger-Global' AND ad_group_criterion.status = 'ENABLED'
          AND segments.date DURING LAST_14_DAYS
        ORDER BY metrics.impressions DESC LIMIT 10
    """
    print("\nTop 10 Keywords by Impressions:")
    try:
        stream = ga_service.search_stream(customer_id=customer_id, query=q_kw)
        for batch in stream:
            for row in batch.results:
                kw = row.ad_group_criterion.keyword.text
                ag = row.ad_group.name
                impr = row.metrics.impressions
                qs = row.ad_group_criterion.quality_info.quality_score
                imp_share = row.metrics.search_impression_share
                print(f"KW: [{kw}] (in {ag}) | Impr: {impr} | ImpShare: {imp_share} | QS: {qs}/10")
    except Exception as e:
        print(f"Error querying keywords: {e}")

if __name__ == '__main__':
    update_mock_budget()
    analyze_swagger()
