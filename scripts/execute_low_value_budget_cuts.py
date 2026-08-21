import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

client = GoogleAdsClient.load_from_storage(r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml")
customer_id = "9496728294"

def get_campaign(campaign_name):
    query = f"""
        SELECT campaign.id, campaign.name, campaign.campaign_budget 
        FROM campaign 
        WHERE campaign.name = '{campaign_name}'
    """
    response = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=query)
    for row in response:
        return row.campaign
    return None

def get_budget(budget_id):
    query = f"SELECT campaign_budget.id, campaign_budget.amount_micros FROM campaign_budget WHERE campaign_budget.id = {budget_id}"
    response = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=query)
    for row in response:
        return row.campaign_budget
    return None

cut_plan = {
    "Google-Sa-Swagger-Global": 0.80, # Reduce 20%
    "Google-Sa-Mintlify-Global": 0.85, # Reduce 15%
    "Google-Sa-MCP-Infrastructure": 0.85, # Reduce 15%
    "Google-Sa-Func-CICD-Global": 0.85 # Reduce 15%
}

budget_operations = []
budget_service = client.get_service("CampaignBudgetService")

for name, ratio in cut_plan.items():
    camp = get_campaign(name)
    if camp:
        budget = get_budget(camp.campaign_budget.split('/')[-1])
        if budget:
            # Calculate new amount and round to the nearest cent (multiple of 10000 micros)
            new_amount = int(round(budget.amount_micros * ratio / 10000.0)) * 10000
            
            budget_op = client.get_type("CampaignBudgetOperation")
            budget_op.update.resource_name = budget.resource_name
            budget_op.update.amount_micros = new_amount
            client.copy_from(budget_op.update_mask, protobuf_helpers.field_mask(None, budget_op.update._pb))
            budget_operations.append(budget_op)
            
            print(f"[{name}] Budget reduced to ${new_amount / 1000000:.2f}")

if budget_operations:
    try:
        response = budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=budget_operations)
        print("Budget reduction updates successful.")
    except Exception as e:
        print(f"Error during budget updates: {e}")
