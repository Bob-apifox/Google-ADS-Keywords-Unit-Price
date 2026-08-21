import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
campaign_service = client.get_service('CampaignService')
campaign_budget_service = client.get_service('CampaignBudgetService')
customer_id = '9496728294'

query = """
    SELECT campaign.id, campaign.name, campaign_budget.resource_name, campaign_budget.amount_micros
    FROM campaign
    WHERE campaign.name = 'Google-Sa-CP-Global'
"""
response = ga_service.search(customer_id=customer_id, query=query)

for row in response:
    budget_resource_name = row.campaign_budget.resource_name
    old_budget = row.campaign_budget.amount_micros / 1e6
    print(f"[{row.campaign.name}] Current Budget: ${old_budget}")

    new_budget_micros = 300 * 1000000
    
    budget_operation = client.get_type("CampaignBudgetOperation")
    budget_update = budget_operation.update
    budget_update.resource_name = budget_resource_name
    budget_update.amount_micros = new_budget_micros
    client.copy_from(budget_operation.update_mask, protobuf_helpers.field_mask(None, budget_update._pb))
    
    budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[budget_operation]
    )
    print(f"Successfully updated budget to $300 for {row.campaign.name}")
