import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"
MINTLIFY_CAMPAIGN_ID = "23320166856"

# 1. Update Budgets
budgets_to_update = {
    "14105204843": 335.4, # CP-Global (258 * 1.3)
    "14183378351": 62.4,  # DSA-Postman (48 * 1.3)
    "15261812542": 19.5,  # Fern-Global (15 * 1.3)
    "15506317155": 65.0   # Category-Competitor (50 * 1.3)
}

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)

campaign_budget_service = client.get_service("CampaignBudgetService")
budget_operations = []

for budget_id, new_amount in budgets_to_update.items():
    op = client.get_type("CampaignBudgetOperation")
    budget = op.update
    budget.resource_name = campaign_budget_service.campaign_budget_path(CUSTOMER_ID, budget_id)
    budget.amount_micros = int(new_amount * 1000000)
    
    # Create a field mask
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, budget._pb))
    budget_operations.append(op)

try:
    print("Executing budget updates...")
    budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=CUSTOMER_ID, operations=budget_operations
    )
    for result in budget_response.results:
        print(f"Updated Budget: {result.resource_name}")
except Exception as e:
    print(f"Budget update failed: {e}")


# 2. Add Negative Keywords to Mintlify
negative_keywords = [
    "code editing redefined",
    "lovable",
    "online api test",
    "llama coder",
    "docsumo",
    "community edition ce",
    "web check ai",
    "webstorm intellij idea",
    "markdown",
    "bubble no code"
]

campaign_criterion_service = client.get_service("CampaignCriterionService")
campaign_service = client.get_service("CampaignService")
criterion_operations = []

for word in negative_keywords:
    op = client.get_type("CampaignCriterionOperation")
    criterion = op.create
    criterion.campaign = campaign_service.campaign_path(CUSTOMER_ID, MINTLIFY_CAMPAIGN_ID)
    criterion.negative = True
    criterion.keyword.text = word
    criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE

    criterion_operations.append(op)

try:
    print("Adding negative keywords to Mintlify...")
    crit_response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=CUSTOMER_ID, operations=criterion_operations
    )
    for result in crit_response.results:
        print(f"Added negative keyword: {result.resource_name}")
except Exception as e:
    print(f"Negative keyword addition failed: {e}")
