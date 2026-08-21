import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

def execute():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    camp_service = client.get_service('CampaignService')
    budget_service = client.get_service('CampaignBudgetService')

    camp_names = [
        'Google-Sa-Testing-Global',
        'Google-Sa-Doc-Global',
        'Google-Sa-Bruno-Global',
        'Google-Sa-Solutions-AI-LLM-Global',
        'Google-Sa-CP-ID',
        'Google-PMax-CP-Global',
        'Google-Sa-RapidAPI-Global'
    ]
    
    camps_sql = ", ".join([f"'{c}'" for c in camp_names])
    query = f"""
        SELECT 
            campaign.resource_name,
            campaign.name, 
            campaign.campaign_budget,
            campaign_budget.resource_name,
            campaign_budget.amount_micros,
            campaign.target_cpa.target_cpa_micros,
            campaign.maximize_conversions.target_cpa_micros
        FROM campaign 
        WHERE campaign.name IN ({camps_sql})
    """
    
    # Define targets
    adjustments = {
        'Google-Sa-Testing-Global': {'budget': 70.0, 'tcpa': 1.20},
        'Google-Sa-Doc-Global': {'budget': 11.25, 'tcpa': 2.00},
        'Google-Sa-Bruno-Global': {'budget': 7.50, 'tcpa': 2.00},
        'Google-Sa-Solutions-AI-LLM-Global': {'budget': 140.0, 'tcpa': 1.58},
        'Google-Sa-CP-ID': {'budget': 32.5, 'tcpa': 1.24},
        'Google-Sa-RapidAPI-Global': {'budget': 37.5, 'tcpa': 0.96},
        'Google-PMax-CP-Global': {'budget': 37.5, 'tcpa': None} # No tCPA
    }

    camp_ops = []
    budget_ops = []
    
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            name = row.campaign.name
            adj = adjustments.get(name)
            if not adj: continue
            
            # 1. Update Budget
            if row.campaign_budget:
                b_op = client.get_type("CampaignBudgetOperation")
                b = b_op.update
                b.resource_name = row.campaign_budget.resource_name
                b.amount_micros = int(adj['budget'] * 1000000)
                b_op.update_mask.paths.append("amount_micros")
                budget_ops.append(b_op)
                
            # 2. Update tCPA
            if adj['tcpa'] is not None:
                c_op = client.get_type("CampaignOperation")
                c = c_op.update
                c.resource_name = row.campaign.resource_name
                
                # Check which strategy it uses
                if row.campaign.target_cpa.target_cpa_micros:
                    c.target_cpa.target_cpa_micros = int(adj['tcpa'] * 1000000)
                    c_op.update_mask.paths.append("target_cpa.target_cpa_micros")
                    camp_ops.append(c_op)
                elif row.campaign.maximize_conversions.target_cpa_micros:
                    c.maximize_conversions.target_cpa_micros = int(adj['tcpa'] * 1000000)
                    c_op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
                    camp_ops.append(c_op)

    if budget_ops:
        try:
            budget_resp = budget_service.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=budget_ops)
            print(f"Updated {len(budget_resp.results)} budgets.")
        except Exception as e:
            print(f"Failed to update budgets: {e}")
            
    if camp_ops:
        try:
            camp_resp = camp_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=camp_ops)
            print(f"Updated {len(camp_resp.results)} tCPA targets.")
        except Exception as e:
            print(f"Failed to update tCPAs: {e}")

if __name__ == '__main__':
    execute()
