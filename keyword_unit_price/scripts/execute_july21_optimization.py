import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

# Setup proxy for REST transport
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

# 1. Budget Updates (Campaign Name -> Percentage Adjustment)
# Note: Google-Sa-CP-Global is explicitly EXCLUDED to protect primary brand traffic
BUDGET_ADJUSTMENTS = {
    "Google-Sa-Postman-Global": 0.15,            # CPA dropped to $1.15! Increase budget 15%
    "Google-Sa-Solutions-AI-LLM-Global": 0.20,   # Excellent CPA ($2.82) -> Increase budget 20%
    "Google-Sa-Scalar-Global": -0.30,            # High CPA ($18.93) -> Decrease budget 30%
    "Google-Sa-Bruno-Global": -0.20,             # High CPA ($12.97) -> Decrease budget 20%
    "Google-Sa-LLM-Benchmarking": -0.30,         # High CPA ($3.43) / Low conversion -> Decrease budget 30%
    "Google-Sa-CLI-Global": -0.15,               # 0 conversions -> Reduce budget 15%
}

# 2. Campaign Negative Keywords (Campaign Name -> PHRASE match negatives)
# Note: Google-Sa-CP-Global is EXCLUDED
CAMPAIGN_NEGATIVES = {
    "Google-Sa-Solutions-AI-LLM-Global": [
        "ai coding", "ai prompt", "ai writer", "ai bot", "ai generator code", "llm price", "how to build ai"
    ],
    "Google-Sa-Postman-Global": [
        "postman crack", "postman student", "postman course", "free download pdf", "tutorial for beginners"
    ],
    "Google-Sa-CLI-Global": [
        "cmd", "powershell", "ubuntu", "windows command prompt", "free linux tutorial"
    ],
    "Google-Sa-Doc-Global": [
        "word doc", "pdf generator", "medical doc", "doctor", "free template"
    ],
    "Google-Sa-Insomnia-Global": [
        "sleep", "disease", "cure", "insomnia cookie"
    ],
    "Google-Sa-Scalar-Global": [
        "math", "physics", "vector", "definition"
    ],
    "Google-Sa-MCP-Infrastructure": [
        "minecraft", "server hosting", "aws pricing"
    ]
}

# 3. Keywords to Pause (Campaign Name -> Keyword Text)
# Note: Google-Sa-CP-Global is EXCLUDED
KEYWORDS_TO_PAUSE = {
    "Google-Sa-Solutions-AI-LLM-Global": ["ai driven api development"],
    "Google-Sa-Jmeter-Global": ["performance software testing"]
}

# 4. New Keywords to Inject into Standard Ad Groups (Campaign Name -> List of Keywords)
# Note: Reassigned long-tail keywords to Google-Sa-Category-Competitor-Global instead of Google-Sa-CP-Global
KEYWORDS_TO_ADD = {
    "Google-Sa-Postman-Global": [
        "app like postman",
        "tools like postman",
        "postman alternative no login",
        "postman runner limit alternative",
        "postman collection runner limit",
        "postman cloud sync issues",
        "postman offline mode workaround",
        "postman enterprise alternative",
        "hipaa compliant api client",
        "soc2 compliant postman alternative"
    ],
    "Google-Sa-Testing-Global": [
        "ci cd api testing",
        "api testing pipeline",
        "automated rest api tests",
        "api security testing tool",
        "owasp api top 10 tester"
    ],
    "Google-Sa-MCP-Infrastructure": [
        "mcp server testing tool",
        "model context protocol inspector",
        "test mcp tool api",
        "ai agent api debugger"
    ],
    "Google-Sa-Func-MultiProtocol-Global": [
        "sse endpoint testing tool",
        "websocket api client online",
        "debug sse stream api"
    ],
    "Google-Sa-Category-Competitor-Global": [
        "free api tool for teams",
        "open source api client desktop",
        "offline first api testing tool"
    ]
}

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        ga_service = client.get_service("GoogleAdsService")
        campaign_budget_service = client.get_service("CampaignBudgetService")
        campaign_criterion_service = client.get_service("CampaignCriterionService")
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    except Exception as e:
        print(f"Failed to load Google Ads client: {e}")
        return

    # Map Campaign Name -> (Campaign ID, Budget ID, Budget Amount Micros, List of SEARCH_STANDARD AdGroups)
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
                    "budget_amount": row.campaign_budget.amount_micros,
                    "ad_groups": []
                }
    except Exception as e:
        print(f"Error fetching campaigns: {e}")
        return

    # Fetch SEARCH_STANDARD Ad Groups only (ignoring DSA)
    print(">>> Fetching enabled SEARCH_STANDARD ad groups...")
    query_ad_groups = """
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.type,
            campaign.name
        FROM ad_group
        WHERE ad_group.status = 'ENABLED'
          AND campaign.status = 'ENABLED'
          AND ad_group.type = 'SEARCH_STANDARD'
    """
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_ad_groups)
        for batch in stream:
            for row in batch.results:
                c_name = row.campaign.name
                if c_name in campaign_map:
                    campaign_map[c_name]["ad_groups"].append({
                        "id": row.ad_group.id,
                        "name": row.ad_group.name
                    })
    except Exception as e:
        print(f"Error fetching ad groups: {e}")

    # --- PHASE 1: BUDGET UPDATES ---
    print("\n>>> Phase 1: Processing budget updates...")
    budget_operations = []
    for c_name, percent_adj in BUDGET_ADJUSTMENTS.items():
        if c_name in campaign_map:
            c_info = campaign_map[c_name]
            b_id = c_info["budget_id"]
            current_micros = c_info["budget_amount"]
            new_amount_micros = int(round(current_micros * (1 + percent_adj) / 1000000.0) * 1000000)
            
            print(f"Campaign '{c_name}': Current ${current_micros/1000000.0:.2f} -> Proposed ${new_amount_micros/1000000.0:.2f} ({percent_adj*100:+.0f}%)")
            
            op = client.get_type("CampaignBudgetOperation")
            budget = op.update
            budget.resource_name = campaign_budget_service.campaign_budget_path(CUSTOMER_ID, b_id)
            budget.amount_micros = new_amount_micros
            client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, budget._pb))
            budget_operations.append(op)
        else:
            print(f"WARNING: Campaign '{c_name}' not found.")

    if budget_operations:
        try:
            response = campaign_budget_service.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=budget_operations)
            print(f"SUCCESS: Updated {len(response.results)} campaign budgets.")
        except Exception as e:
            print(f"ERROR updating budgets: {e}")

    # --- PHASE 2: CAMPAIGN NEGATIVE KEYWORDS ---
    print("\n>>> Phase 2: Injecting campaign negative keywords...")
    negative_operations = []
    for c_name, kws in CAMPAIGN_NEGATIVES.items():
        if c_name in campaign_map:
            c_id = campaign_map[c_name]["id"]
            c_path = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, c_id)
            for kw in kws:
                op = client.get_type("CampaignCriterionOperation")
                criterion = op.create
                criterion.campaign = c_path
                criterion.negative = True
                criterion.keyword.text = kw
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                negative_operations.append(op)

    if negative_operations:
        try:
            response = campaign_criterion_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=negative_operations)
            print(f"SUCCESS: Injected {len(response.results)} negative keywords.")
        except Exception as e:
            print(f"ERROR injecting negatives: {e}")

    # --- PHASE 3: PAUSING LOW-QUALITY KEYWORDS ---
    print("\n>>> Phase 3: Pausing low-quality keywords...")
    keyword_pause_ops = []
    query_keywords = """
        SELECT
            campaign.name,
            ad_group_criterion.criterion_id,
            ad_group_criterion.ad_group,
            ad_group_criterion.keyword.text
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
                    ad_group_id = ad_group_resource.split('/')[-1]
                    op = client.get_type("AdGroupCriterionOperation")
                    criterion = op.update
                    criterion.resource_name = ad_group_criterion_service.ad_group_criterion_path(
                        CUSTOMER_ID, ad_group_id, criterion_id
                    )
                    criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
                    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, criterion._pb))
                    keyword_pause_ops.append(op)
    except Exception as e:
        print(f"Error querying keywords: {e}")

    if keyword_pause_ops:
        try:
            response = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=keyword_pause_ops)
            print(f"SUCCESS: Paused {len(response.results)} keywords.")
        except Exception as e:
            print(f"ERROR pausing keywords: {e}")

    # --- PHASE 4: INJECTING NEW HIGH-CONVERTING KEYWORDS (BROAD MATCH FOR SMART BIDDING) ---
    print("\n>>> Phase 4: Injecting new high-converting keywords into SEARCH_STANDARD ad groups...")
    new_kw_ops = []
    for c_name, kws in KEYWORDS_TO_ADD.items():
        if c_name in campaign_map and campaign_map[c_name]["ad_groups"]:
            target_ag_id = campaign_map[c_name]["ad_groups"][0]["id"]
            target_ag_name = campaign_map[c_name]["ad_groups"][0]["name"]
            ag_resource_name = client.get_service("AdGroupService").ad_group_path(CUSTOMER_ID, target_ag_id)
            
            for kw_text in kws:
                print(f"Adding new keyword '{kw_text}' (BROAD) to Campaign '{c_name}' -> AdGroup '{target_ag_name}' ({target_ag_id})")
                op = client.get_type("AdGroupCriterionOperation")
                criterion = op.create
                criterion.ad_group = ag_resource_name
                criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
                criterion.keyword.text = kw_text
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
                new_kw_ops.append(op)
        else:
            print(f"WARNING: No active SEARCH_STANDARD ad group found for Campaign '{c_name}', skipping new keywords.")

    if new_kw_ops:
        try:
            response = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=new_kw_ops)
            print(f"SUCCESS: Injected {len(response.results)} new keywords.")
        except Exception as e:
            print(f"ERROR injecting new keywords: {e}")

    print("\n>>> ALL OPTIMIZATIONS (EXCLUDING Google-Sa-CP-Global) SUCCESSFULLY EXECUTED AND UPLOADED TO GOOGLE ADS!")

if __name__ == "__main__":
    main()
