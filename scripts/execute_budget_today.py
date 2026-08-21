import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
campaign_budget_service = client.get_service('CampaignBudgetService')
customer_id = '9496728294'

increases = {
    'Google-Sa-CP-AR': 1.50, # +50%
    'Google-Sa-CP-ID': 1.30, # +30%
    'Google-Sa-CP-VN': 1.30, # +30%
    'Google-Sa-DSA-Global': 1.40 # +40%
}

q = "SELECT campaign.name, campaign.campaign_budget FROM campaign WHERE campaign.status != 'REMOVED'"
stream = ga_service.search_stream(customer_id=customer_id, query=q)

budget_resource_names = {}
for batch in stream:
    for row in batch.results:
        camp_name = row.campaign.name
        if camp_name in increases:
            budget_resource_names[camp_name] = row.campaign.campaign_budget

if not budget_resource_names:
    print("No matching campaigns found for budget increase.")
    exit()

# Now fetch the actual budgets to calculate the new amounts
b_q = f"SELECT campaign_budget.resource_name, campaign_budget.amount_micros FROM campaign_budget"
b_stream = ga_service.search_stream(customer_id=customer_id, query=b_q)

budget_amounts = {}
for batch in b_stream:
    for row in batch.results:
        budget_amounts[row.campaign_budget.resource_name] = row.campaign_budget.amount_micros

operations = []
from google.api_core import protobuf_helpers

for camp_name, multiplier in increases.items():
    if camp_name not in budget_resource_names:
        print(f"Warning: Campaign {camp_name} not found.")
        continue
    
    res_name = budget_resource_names[camp_name]
    current_micros = budget_amounts.get(res_name)
    if not current_micros:
        print(f"Warning: Could not fetch current budget for {camp_name}.")
        continue
        
    new_micros = int(round((current_micros * multiplier) / 10000) * 10000)
    print(f"[{camp_name}] Increasing budget: {current_micros/1e6:.2f} -> {new_micros/1e6:.2f}")
    
    operation = client.get_type('CampaignBudgetOperation')
    budget = operation.update
    budget.resource_name = res_name
    budget.amount_micros = new_micros
    
    fm = protobuf_helpers.field_mask(None, type(budget).pb(budget))
    client.copy_from(operation.update_mask, fm)
    operations.append(operation)

if operations:
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=operations
    )
    print(f"Successfully updated {len(response.results)} budgets.")
