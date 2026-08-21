import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
campaign_budget_service = client.get_service('CampaignBudgetService')
customer_id = '9496728294'

budget_updates = {
    'Google-Sa-Insomnia-Global': 45.0,
    'Google-Sa-Hoppscotch-Global': 60.0,
    'Google-Sa-Mintlify-Global': 75.0,
    'Google-Sa-Jmeter-Global': 65.0,
    'Google-Sa-Readme-Global': 40.0,
    'Google-Sa-Mock-Global': 25.0,
    'Google-Sa-Stoplight-Global': 30.0,
    'Google-Sa-Debug-Global': 25.0,
    'Google-Sa-Openapi-Global': 25.0,
    'Google-Sa-Expansion-Horizon-2026': 25.0,
    'Google-Sa-Doc-Global': 15.0,
    'Google-Sa-API Editor-Global': 15.0,
    'Google-Sa-Solutions-Unified-API-Global': 20.0,
    'Google-Sa-Annual Planning & New Trends': 35.0,
    'Google-Sa-Bruno-Global': 10.0,
    'Google-Sa-Scalar-Global': 10.0,
    'Google-Sa-LLM-Benchmarking': 10.0,
    'Google-Sa-CLI-Global': 10.0
}

# Fetch the campaign budget resource names
query = """
    SELECT campaign.id, campaign.name, campaign_budget.resource_name, campaign_budget.amount_micros
    FROM campaign
    WHERE campaign.status = 'ENABLED'
"""
response = ga_service.search(customer_id=customer_id, query=query)

operations = []
for row in response:
    camp_name = row.campaign.name
    if camp_name in budget_updates:
        budget_resource_name = row.campaign_budget.resource_name
        new_budget = budget_updates[camp_name]
        new_budget_micros = int(new_budget * 1000000)
        
        budget_operation = client.get_type("CampaignBudgetOperation")
        budget_update = budget_operation.update
        budget_update.resource_name = budget_resource_name
        budget_update.amount_micros = new_budget_micros
        client.copy_from(budget_operation.update_mask, protobuf_helpers.field_mask(None, budget_update._pb))
        
        operations.append(budget_operation)
        print(f"Prepared operation for {camp_name}: -> ${new_budget}")

if operations:
    budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=operations
    )
    print(f"Successfully updated {len(operations)} campaign budgets!")
else:
    print("No operations to execute.")
