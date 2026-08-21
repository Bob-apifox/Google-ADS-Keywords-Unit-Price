import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers
# Setup proxy for REST transport
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

# 1. Budget updates (Name -> Percentage Adjustment)
# e.g., -0.30 means decrease by 30%, 0.20 means increase by 20%
BUDGET_ADJUSTMENTS = {
    "Google-Sa-CLI-Global": -0.30,               # 0 conversions, high spend -> Reduce 30%
    "Google-Sa-Doc-Global": -0.20,               # High CPA ($15.24) -> Reduce 20%
    "Google-Sa-Insomnia-Global": -0.15,          # High CPA ($7.35) -> Reduce 15%
    "Google-Sa-Scalar-Global": -0.15,            # High CPA ($7.14) -> Reduce 15%
    "Google-Sa-Readme-Global": -0.15,            # High CPA ($6.33) -> Reduce 15%
    "Google-Sa-DSA-Postman-Global": -0.10,       # High CPA ($5.90) -> Reduce 10%
    "Google-Sa-Solutions-AI-LLM-Global": 0.20,   # Excellent CPA ($0.46) -> Increase 20%
}

# 2. Campaign negative keywords to inject (Campaign Name -> Keywords to add as PHRASE match)
CAMPAIGN_NEGATIVES = {
    "Google-Sa-CLI-Global": [
        "terminal api tester", "cmd", "linux", "windows", "powershell", "bash", "ubuntu", "command prompt"
    ],
    "Google-Sa-Doc-Global": [
        "template", "free", "example", "google docs", "word doc", "pdf generator", "medical doc", "doctor"
    ],
    "Google-Sa-Postman-Global": [
        "crack", "free", "tutorial", "course", "delivery", "mail", "pat", "student", "open source"
    ],
    "Google-Sa-DSA-Postman-Global": [
        "crack", "free", "student", "delivery", "mail"
    ],
    "Google-Sa-Insomnia-Global": [
        "crack", "free", "cookie", "sleep", "disease", "cure", "open source", "rest api tutorial"
    ],
    "Google-Sa-Scalar-Global": [
        "free", "math", "physics", "quantity", "definition", "vector"
    ],
    "Google-Sa-Readme-Global": [
        "free", "template", "github readme", "markdown editor", "how to write"
    ],
    "Google-Sa-Swagger-Global": [
        "free", "tutorial", "clothing", "meaning", "definition", "open source"
    ],
    "Google-Sa-LLM-Benchmarking": [
        "free", "gpu", "nvidia", "hardware"
    ],
    "Google-Sa-MCP-Infrastructure": [
        "free", "minecraft", "server hosting", "aws pricing"
    ],
    "Google-Sa-Stoplight-Global": [
        "free", "traffic stoplight", "meaning", "studio open source"
    ],
    "Google-Sa-Jmeter-Global": [
        "free", "apache", "open source", "tutorial"
    ],
    "Google-Sa-CP-Global": [
        "uipath", "devtools", "buffer api", "onlinepostman", "dog food", "pet api"
    ],
    "Google-Sa-API Editor-Global": [
        "free", "video", "photo", "text", "code editor", "vs code"
    ],
    "Google-Sa-Design-Global": [
        "free", "graphic", "logo", "figma", "sketch", "photoshop"
    ]
}

# 3. Keywords to pause (Campaign Name -> Keywords to pause)
KEYWORDS_TO_PAUSE = {
    "Google-Sa-CP-Global": ["apidog download"] # Pausing the Broad Match version due to high CPC and waste
}

def main():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        ga_service = client.get_service("GoogleAdsService")
        campaign_criterion_service = client.get_service("CampaignCriterionService")
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    except Exception as e:
        print(f"Failed to load Google Ads client: {e}")
        return
    
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
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_campaigns)
        for batch in stream:
            for row in batch.results:
                c_name = row.campaign.name
                campaign_map[c_name] = {
                    "id": row.campaign.id,
                    "budget_id": row.campaign_budget.id,
                    "budget_amount": row.campaign_budget.amount_micros
                }
    except Exception as e:
        print(f"Error fetching campaigns (is proxy running?): {e}")
        return
        
    # --- PHASE 1: BUDGET UPDATES ---
    print("\n>>> Processing budget updates...")
    campaign_budget_service = client.get_service("CampaignBudgetService")
    budget_operations = []
    for c_name, percent_adj in BUDGET_ADJUSTMENTS.items():
        if c_name in campaign_map:
            c_info = campaign_map[c_name]
            b_id = c_info["budget_id"]
            current_micros = c_info["budget_amount"]
            
            # Calculate new budget (rounded to nearest whole dollar/currency unit)
            new_amount_micros = int(round(current_micros * (1 + percent_adj) / 1000000.0) * 1000000)
            
            print(f"Campaign '{c_name}': Current budget {current_micros/1000000.0:.2f} USD -> Proposed {new_amount_micros/1000000.0:.2f} USD ({percent_adj*100:+.0f}%)")
            
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
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_keywords)
        for batch in stream:
            for row in batch.results:
                c_name = row.campaign.name
                kw_text = row.ad_group_criterion.keyword.text
                ad_group_resource = row.ad_group_criterion.ad_group
                criterion_id = row.ad_group_criterion.criterion_id
                
                if c_name in KEYWORDS_TO_PAUSE and kw_text in KEYWORDS_TO_PAUSE[c_name]:
                    print(f"Pausing keyword '{kw_text}' in Campaign '{c_name}'")
                    
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
    except Exception as e:
         print(f"Error fetching keywords: {e}")
                
    if keyword_operations:
        try:
            print(f"Executing {len(keyword_operations)} keyword pauses...")
            response = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=keyword_operations)
            print(f"SUCCESS: Paused {len(response.results)} keywords.")
        except Exception as e:
            print(f"ERROR pausing keywords: {e}")
    else:
        print("No keywords need to be paused found.")
        
    print("\n>>> ALL OPTIMIZATIONS COMPLETED.")

if __name__ == "__main__":
    main()
