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
        SELECT campaign.id, campaign.name, campaign.campaign_budget, campaign.target_cpa.target_cpa_micros 
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

campaigns_to_boost = [
    "Google-Sa-DSA-Global",
    "Google-Sa-Readme-Global",
    "Google-Sa-Expansion-Horizon-2026",
    "Google-Sa-Solutions-Unified-API-Global",
    "Google-Sa-API Editor-Global"
]

tcpa_adjustments = {
    "Google-Sa-Readme-Global": 1800000, # $1.80
    "Google-Sa-API Editor-Global": 1800000 # $1.80
}

budget_operations = []
campaign_operations = []

campaign_service = client.get_service("CampaignService")
budget_service = client.get_service("CampaignBudgetService")

for name in campaigns_to_boost:
    camp = get_campaign(name)
    if camp:
        # Increase Budget by 20%
        budget = get_budget(camp.campaign_budget.split('/')[-1])
        if budget:
            new_amount = int(round(budget.amount_micros * 1.20 / 10000.0)) * 10000
            budget_op = client.get_type("CampaignBudgetOperation")
            budget_op.update.resource_name = budget.resource_name
            budget_op.update.amount_micros = new_amount
            client.copy_from(budget_op.update_mask, protobuf_helpers.field_mask(None, budget_op.update._pb))
            budget_operations.append(budget_op)
            print(f"[{name}] Budget increased to ${new_amount / 1000000:.2f}")

        # Set specific tCPA if present in dictionary
        if name in tcpa_adjustments:
            new_tcpa = tcpa_adjustments[name]
            camp_op = client.get_type("CampaignOperation")
            camp_op.update.resource_name = camp.resource_name
            camp_op.update.maximize_conversions.target_cpa_micros = new_tcpa
            client.copy_from(camp_op.update_mask, protobuf_helpers.field_mask(None, camp_op.update._pb))
            campaign_operations.append(camp_op)
            print(f"[{name}] tCPA updated to ${new_tcpa / 1000000:.2f}")

if budget_operations:
    response = budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=budget_operations)
    print("Budget updates successful.")
if campaign_operations:
    response = campaign_service.mutate_campaigns(customer_id=customer_id, operations=campaign_operations)
    print("Campaign tCPA updates successful.")
