import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

def execute():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')

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
            campaign.id, 
            campaign.name, 
            campaign.campaign_budget,
            campaign_budget.amount_micros,
            campaign.target_cpa.target_cpa_micros,
            campaign.maximize_conversions.target_cpa_micros
        FROM campaign 
        WHERE campaign.name IN ({camps_sql})
    """
    
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            budget = row.campaign_budget.amount_micros / 1000000.0 if row.campaign_budget else 0
            tcpa1 = row.campaign.target_cpa.target_cpa_micros
            tcpa2 = row.campaign.maximize_conversions.target_cpa_micros
            tcpa = (tcpa1 or tcpa2)
            tcpa_val = tcpa / 1000000.0 if tcpa else 0
            
            print(f"Campaign: {row.campaign.name}")
            print(f"  Budget: ${budget}")
            print(f"  tCPA: ${tcpa_val}")
            print(f"  Budget Resource: {row.campaign_budget.resource_name if row.campaign_budget else 'None'}")
            print("-" * 20)

if __name__ == '__main__':
    execute()
