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
        SELECT campaign.id, campaign.name, campaign.campaign_budget, campaign.target_cpa.target_cpa_micros, campaign.maximize_conversions.target_cpa_micros 
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

campaign_adjustments = {
    'Google-Sa-Insomnia-Global': {'budget_multiplier': 0.60, 'tcpa_multiplier': 0.85},
    'Google-Sa-CLI-Terminal-Global': {'budget_multiplier': 0.70, 'tcpa_multiplier': 1.0},
    'Google-Sa-Func-MultiProtocol-Global': {'budget_multiplier': 0.70, 'tcpa_multiplier': 1.0},
    'Google-Sa-Stoplight-Global': {'budget_multiplier': 0.80, 'tcpa_multiplier': 1.0},
    
    'Google-Sa-Comp-HeavyQA-Global': {'budget_multiplier': 1.15, 'tcpa_multiplier': 1.05},
    'Google-Sa-Hoppscotch-Global': {'budget_multiplier': 1.15, 'tcpa_multiplier': 1.05},
    'Google-Sa-Postman-Global': {'budget_multiplier': 1.15, 'tcpa_multiplier': 1.05},
    
    'Google-Sa-Jmeter-Global': {'budget_multiplier': 1.10, 'tcpa_multiplier': 1.0},
    'Google-Sa-Annual Planning & New Trends-26': {'budget_multiplier': 1.10, 'tcpa_multiplier': 1.0},
    'Google-PMax-CP-Global': {'budget_multiplier': 1.15, 'tcpa_multiplier': 1.0},
}

budget_operations = []
campaign_operations = []
campaign_service = client.get_service("CampaignService")
budget_service = client.get_service("CampaignBudgetService")

for name, multipliers in campaign_adjustments.items():
    camp = get_campaign(name)
    if camp:
        budget = get_budget(camp.campaign_budget.split('/')[-1])
        if budget:
            new_amount = int(round(budget.amount_micros * multipliers['budget_multiplier'] / 10000.0)) * 10000
            budget_op = client.get_type("CampaignBudgetOperation")
            budget_op.update.resource_name = budget.resource_name
            budget_op.update.amount_micros = new_amount
            client.copy_from(budget_op.update_mask, protobuf_helpers.field_mask(None, budget_op.update._pb))
            budget_operations.append(budget_op)
            print(f"Budget for {name} updated to {new_amount / 1000000}")
        
        if multipliers['tcpa_multiplier'] != 1.0:
            camp_op = client.get_type("CampaignOperation")
            camp_op.update.resource_name = camp.resource_name
            if camp.target_cpa.target_cpa_micros:
                new_tcpa = int(round(camp.target_cpa.target_cpa_micros * multipliers['tcpa_multiplier'] / 10000.0)) * 10000
                camp_op.update.target_cpa.target_cpa_micros = new_tcpa
                client.copy_from(camp_op.update_mask, protobuf_helpers.field_mask(None, camp_op.update._pb))
                campaign_operations.append(camp_op)
                print(f"tCPA for {name} updated to {new_tcpa / 1000000}")
            elif camp.maximize_conversions.target_cpa_micros:
                new_tcpa = int(round(camp.maximize_conversions.target_cpa_micros * multipliers['tcpa_multiplier'] / 10000.0)) * 10000
                camp_op.update.maximize_conversions.target_cpa_micros = new_tcpa
                client.copy_from(camp_op.update_mask, protobuf_helpers.field_mask(None, camp_op.update._pb))
                campaign_operations.append(camp_op)
                print(f"tCPA (Max Conv) for {name} updated to {new_tcpa / 1000000}")

# Setting specific tCPA for PMax-Postman
camp = get_campaign('Google-PMax-Postman')
if camp:
    camp_op = client.get_type("CampaignOperation")
    camp_op.update.resource_name = camp.resource_name
    camp_op.update.maximize_conversions.target_cpa_micros = 4500000 # $4.50
    client.copy_from(camp_op.update_mask, protobuf_helpers.field_mask(None, camp_op.update._pb))
    campaign_operations.append(camp_op)
    print(f"Set tCPA for Google-PMax-Postman to 4.5")

if budget_operations:
    response = budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=budget_operations)
    print("Budget updates successful.")
if campaign_operations:
    response = campaign_service.mutate_campaigns(customer_id=customer_id, operations=campaign_operations)
    print("Campaign tCPA updates successful.")

# Negative Keywords
negative_keywords = {
    'Google-Sa-Insomnia-Global': ['"pwa progressive web app"', '"mobile app development"', '"app js"', '"insomnia api"', '"v0 by vercel"', '"glide apps"', '"pwabuilder"'],
    'Google-Sa-CLI-Terminal-Global': ['"online postman"', '"postman online web"', '"postman web"'],
    'Google-Sa-Func-MultiProtocol-Global': ['"websocket"', '"download postman"', '"postman desktop"', '"dio websocket"', '"websocket online"'],
    'Google-Sa-Stoplight-Global': ['"groupdocs"', '"relume"', '"v0 dev bolt new"', '"anthropic console"', '"web bluetooth api"', '"web design software"'],
    'Google-Sa-Func-CICD-Global': ['[github]']
}

criterion_service = client.get_service("CampaignCriterionService")
criterion_ops = []

for name, words in negative_keywords.items():
    camp = get_campaign(name)
    if camp:
        for word in words:
            op = client.get_type("CampaignCriterionOperation")
            criterion = op.create
            criterion.campaign = camp.resource_name
            criterion.negative = True
            
            if word.startswith('[') and word.endswith(']'):
                criterion.keyword.text = word[1:-1]
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
            elif word.startswith('"') and word.endswith('"'):
                criterion.keyword.text = word[1:-1]
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            else:
                criterion.keyword.text = word
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                
            criterion_ops.append(op)

if criterion_ops:
    response = criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=criterion_ops)
    print(f"Added {len(criterion_ops)} negative keywords.")
