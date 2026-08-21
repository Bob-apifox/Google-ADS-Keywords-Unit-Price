import os
import time
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

# Setup proxy
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

# 1. Budgets to update (Name -> New Budget in USD)
BUDGET_UPDATES = {
    "Google-Sa-CP-Global": 340.00,
    "Google-Sa-DSA-Global": 65.00,
    "Google-Sa-Postman-Global": 180.00,
    "Google-Sa-Jmeter-Global": 55.00,
    "Google-Sa-Insomnia-Global": 45.00,
    "Google-Sa-Mintlify-Global": 60.00,
    "Google-Sa-Comp-VSCode-Global": 25.00
}

# 2. Ad groups to pause (Campaign Name -> Ad Group Names)
AD_GROUPS_TO_PAUSE = {
    "Google-Sa-CLI-Global": ["CLI-Competitor-Alternatives"]
}

# 3. Campaign negative keywords to inject (Campaign Name -> Keywords to add as PHRASE match)
CAMPAIGN_NEGATIVES = {
    "Google-Sa-Insomnia-Global": [
        "online api testing", "api test online", "mock api", "software testing", 
        "firebase studio", "wiremock", "playwright", "next js"
    ],
    "Google-Sa-CLI-Global": [
        "postman alternative", "alternative of postman", "postman alternatives", 
        "free api client like postman", "postman online alternative", "postman open source alternative"
    ],
    "Google-Sa-Mintlify-Global": [
        "intellij idea", "pycharm", "run code", "whimsical", "dbeaver", "burp suite"
    ],
    "Google-Sa-Comp-VSCode-Global": [
        "download vscode", "vscode tutorial", "free alternative"
    ]
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    campaign_budget_service = client.get_service("CampaignBudgetService")
    ad_group_service = client.get_service("AdGroupService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    
    # Map Campaign Name -> (Campaign ID, Budget ID, Budget Amount Micros)
    campaign_map = {}
    
    print(">>> Fetching enabled campaigns...")
    query_campaigns = """
        SELECT
            campaign.id,
            campaign.name,
            campaign_budget.id,
            campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_campaigns)
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            campaign_map[c_name] = {
                "id": row.campaign.id,
                "budget_id": row.campaign_budget.id,
                "budget_amount": row.campaign_budget.amount_micros
            }
            
    # --- PHASE 1: BUDGET UPDATES ---
    print("\n>>> Processing budget updates...")
    budget_operations = []
    for c_name, new_budget_usd in BUDGET_UPDATES.items():
        if c_name in campaign_map:
            c_info = campaign_map[c_name]
            b_id = c_info["budget_id"]
            new_amount_micros = int(new_budget_usd * 1000000)
            
            print(f"Campaign '{c_name}': Current budget {c_info['budget_amount']/1000000.0} USD -> Proposed {new_budget_usd} USD")
            
            op = client.get_type("CampaignBudgetOperation")
            budget = op.update
            budget.resource_name = campaign_budget_service.campaign_budget_path(CUSTOMER_ID, b_id)
            budget.amount_micros = new_amount_micros
            client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, budget._pb))
            budget_operations.append(op)
        else:
            print(f"WARNING: Campaign '{c_name}' not found or not enabled.")
            
    if budget_operations:
        try:
            print(f"Executing {len(budget_operations)} budget updates...")
            response = campaign_budget_service.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=budget_operations)
            print(f"SUCCESS: Updated {len(response.results)} budgets.")
        except Exception as e:
            print(f"ERROR updating budgets: {e}")
            
    # --- PHASE 2: AD GROUP PAUSES ---
    print("\n>>> Processing ad group pauses...")
    ad_group_operations = []
    
    # Query all active ad groups for target campaigns
    query_ad_groups = """
        SELECT
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group.status
        FROM ad_group
        WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_ad_groups)
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            ag_name = row.ad_group.name
            ag_id = row.ad_group.id
            
            if c_name in AD_GROUPS_TO_PAUSE and ag_name in AD_GROUPS_TO_PAUSE[c_name]:
                print(f"Pausing Ad Group '{ag_name}' in Campaign '{c_name}'")
                op = client.get_type("AdGroupOperation")
                ag = op.update
                ag.resource_name = ad_group_service.ad_group_path(CUSTOMER_ID, ag_id)
                ag.status = client.enums.AdGroupStatusEnum.PAUSED
                client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, ag._pb))
                ad_group_operations.append(op)
                
    if ad_group_operations:
        try:
            print(f"Executing {len(ad_group_operations)} ad group pauses...")
            response = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=ad_group_operations)
            print(f"SUCCESS: Paused {len(response.results)} ad groups.")
        except Exception as e:
            print(f"ERROR pausing ad groups: {e}")
    else:
        print("No ad groups need to be paused.")

    # --- PHASE 3: CAMPAIGN NEGATIVE KEYWORDS ---
    print("\n>>> Processing campaign negative keywords...")
    negative_operations = []
    
    for c_name, kws in CAMPAIGN_NEGATIVES.items():
        if c_name in campaign_map:
            c_id = campaign_map[c_name]["id"]
            c_path = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, c_id)
            for kw in kws:
                print(f"Adding negative keyword '{kw}' (PHRASE) to Campaign '{c_name}'")
                op = client.get_type("CampaignCriterionOperation")
                criterion = op.create
                criterion.campaign = c_path
                criterion.negative = True
                criterion.keyword.text = kw
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                negative_operations.append(op)
        else:
            print(f"WARNING: Campaign '{c_name}' not found, skipping negative keywords.")
            
    if negative_operations:
        try:
            print(f"Executing {len(negative_operations)} negative keyword additions...")
            response = campaign_criterion_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=negative_operations)
            print(f"SUCCESS: Injected {len(response.results)} negative keywords.")
        except Exception as e:
            print(f"ERROR injecting negative keywords: {e}")
    else:
        print("No negative keywords to inject.")
        
    print("\n>>> ALL OPERATIONS DONE.")

if __name__ == "__main__":
    main()
