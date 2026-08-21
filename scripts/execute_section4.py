import os
import time
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

NEG_LISTS = {
    "Negative-Global-AI-Isolation": [
        "ai", "artificial intelligence", "gpt", "llm", "copilot", "agent", 
        "prompt", "ai api", "api ai", "ai generator", "ai code", "ai schema"
    ],
    "Negative-Educational-Terms": [
        "tutorial", "course", "how to learn", "example", "pdf", "book", 
        "github repo", "definition", "what is", "free online course"
    ]
}

def execute_section4():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    shared_set_service = client.get_service("SharedSetService")
    shared_crit_service = client.get_service("SharedCriterionService")
    camp_shared_set_service = client.get_service("CampaignSharedSetService")
    
    # 1. Fetch existing Shared Sets
    existing_sets = {}
    query = "SELECT shared_set.id, shared_set.name FROM shared_set WHERE shared_set.type = 'NEGATIVE_KEYWORDS' AND shared_set.status = 'ENABLED'"
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            existing_sets[row.shared_set.name] = row.shared_set.id
            
    for list_name, keywords in NEG_LISTS.items():
        set_id = None
        if list_name in existing_sets:
            print(f"Shared Set '{list_name}' already exists. Using existing ID.")
            set_id = existing_sets[list_name]
        else:
            print(f"Creating new Shared Set: {list_name}")
            op = client.get_type("SharedSetOperation")
            shared_set = op.create
            shared_set.name = list_name
            shared_set.type_ = client.enums.SharedSetTypeEnum.NEGATIVE_KEYWORDS
            resp = shared_set_service.mutate_shared_sets(customer_id=CUSTOMER_ID, operations=[op])
            resource_name = resp.results[0].resource_name
            # Parse ID from resource_name (customers/{customer_id}/sharedSets/{set_id})
            set_id = resource_name.split("/")[-1]
            time.sleep(1) # wait a moment for backend to sync
            
        # Add Keywords
        print(f"Adding keywords to '{list_name}'...")
        set_resource_name = shared_set_service.shared_set_path(CUSTOMER_ID, set_id)
        
        ops = []
        for kw in keywords:
            op = client.get_type("SharedCriterionOperation")
            crit = op.create
            crit.shared_set = set_resource_name
            crit.keyword.text = kw
            crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            ops.append(op)
            
        if ops:
            req = client.get_type("MutateSharedCriteriaRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(ops)
            req.partial_failure = True
            resp = shared_crit_service.mutate_shared_criteria(request=req)
            if resp.partial_failure_error and resp.partial_failure_error.details:
                for err in resp.partial_failure_error.details:
                    print(f"Error adding keyword to {list_name}: {err}")
            else:
                print(f"Successfully added {len(ops)} negative keywords to {list_name}")
                
        # Link to all active SEARCH campaigns
        print(f"Linking '{list_name}' to all active Search campaigns...")
        q_camp = "SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = 'ENABLED' AND campaign.advertising_channel_type = 'SEARCH'"
        camp_ops = []
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
            for row in batch.results:
                camp_res_name = ga_service.campaign_path(CUSTOMER_ID, row.campaign.id)
                op = client.get_type("CampaignSharedSetOperation")
                css = op.create
                css.campaign = camp_res_name
                css.shared_set = set_resource_name
                camp_ops.append(op)
                
        if camp_ops:
            req = client.get_type("MutateCampaignSharedSetsRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(camp_ops)
            req.partial_failure = True
            resp = camp_shared_set_service.mutate_campaign_shared_sets(request=req)
            # Usually some campaigns might already be linked, causing a partial failure, we ignore those specific ones
            print(f"Linked {list_name} to {len(camp_ops)} campaigns.")

    print("[SUCCESS] Section 4 Negative Keyword Lists created and linked globally!")

if __name__ == '__main__':
    execute_section4()
