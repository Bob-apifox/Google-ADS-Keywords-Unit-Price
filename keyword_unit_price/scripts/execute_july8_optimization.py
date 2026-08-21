import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

# Setup proxy
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

# 1. Budget reallocation updates (Name -> New Daily Budget in USD)
# - Increase high-performing budget: DSA-Postman-Global (CPA $1.12), Hoppscotch-Global (CPA $3.13)
# - Decrease underperforming budgets: Postman-Global (CPA $15.05), Swagger-Global (CPA N/A)
BUDGET_UPDATES = {
    "Google-Sa-DSA-Postman-Global": 100.00,  # Increase from ~$67 to capture more high-ROI conversions
    "Google-Sa-Hoppscotch-Global": 75.00,    # Increase from ~$53 (CPA $3.13 is very healthy)
    "Google-Sa-Postman-Global": 120.00,      # Decrease from $180 (CPA $15.05 is too high)
    "Google-Sa-CP-Global": 300.00,           # Decrease slightly from $340 to control brand cost (CPA $8.31)
    "Google-Sa-Mintlify-Global": 50.00,      # Decrease from $60 to limit exposure (CPA $6.93)
    "Google-Sa-Stoplight-Global": 20.00      # Decrease slightly (CPA $9.66)
}

# 2. Campaign negative keywords to inject (Campaign Name -> Keywords to add as PHRASE match)
CAMPAIGN_NEGATIVES = {
    "Google-Sa-CP-Global": [
        "uipath", "devtools", "buffer api", "onlinepostman"
    ],
    "Google-Sa-Insomnia-Global": [
        "firebase studio", "wiremock"
    ],
    "Google-Sa-Debug-Global": [
        "replit ghostwriter", "jmeter alternatives", "acode", "firebase studio", "codepen io"
    ],
    "Google-Sa-Mintlify-Global": [
        "intellij idea", "run code", "whimsical", "burp suite"
    ],
    "Google-Sa-Readme-Global": [
        "mermaid js", "kotlin", "draw io", "dillinger io", "fast api"
    ],
    "Google-Sa-SpecFirst-Global": [
        "stoplight elements", "stackblitz", "zapier ai", "tauri"
    ]
}

# 3. Low Quality Score keywords to pause (Campaign Name -> Keywords to pause)
KEYWORDS_TO_PAUSE = {
    "Google-Sa-Swagger-Global": [
        "swagger hub"  # QS is 1
    ],
    "Google-Sa-Openapi-Global": [
        "reqbin"  # QS is 1
    ],
    "Google-Sa-Solutions-Multi-Protocol-Global": [
        "soap api client"  # QS is 1
    ],
    "Google-Sa-RapidAPI-Global": [
        "rapid api"  # QS is 1
    ]
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    
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
            
    # --- PHASE 2: CAMPAIGN NEGATIVE KEYWORDS ---
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
            
    # --- PHASE 3: PAUSING LOW QUALITY KEYWORDS ---
    print("\n>>> Processing keyword pauses...")
    keyword_operations = []
    
    # Query all active keywords for target campaigns
    query_keywords = """
        SELECT
            campaign.name,
            ad_group_criterion.criterion_id,
            ad_group_criterion.ad_group,
            ad_group_criterion.keyword.text,
            ad_group_criterion.status
        FROM ad_group_criterion
        WHERE campaign.status = 'ENABLED' 
          AND ad_group_criterion.status = 'ENABLED'
          AND ad_group_criterion.type = 'KEYWORD'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_keywords)
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            kw_text = row.ad_group_criterion.keyword.text
            ad_group_resource = row.ad_group_criterion.ad_group
            criterion_id = row.ad_group_criterion.criterion_id
            
            if c_name in KEYWORDS_TO_PAUSE and kw_text in KEYWORDS_TO_PAUSE[c_name]:
                print(f"Pausing low-QS keyword '{kw_text}' in Campaign '{c_name}'")
                
                # Fetch ad group ID from resource path
                ad_group_id = ad_group_resource.split('/')[-1]
                
                op = client.get_type("AdGroupCriterionOperation")
                criterion = op.update
                criterion.resource_name = ad_group_criterion_service.ad_group_criterion_path(
                    CUSTOMER_ID, ad_group_id, criterion_id
                )
                criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
                client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, criterion._pb))
                keyword_operations.append(op)
                
    if keyword_operations:
        try:
            print(f"Executing {len(keyword_operations)} keyword pauses...")
            response = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=keyword_operations)
            print(f"SUCCESS: Paused {len(response.results)} keywords.")
        except Exception as e:
            print(f"ERROR pausing keywords: {e}")
    else:
        print("No keywords need to be paused.")
        
    print("\n>>> ALL OPTIMIZATIONS COMPLETED.")

if __name__ == "__main__":
    main()
