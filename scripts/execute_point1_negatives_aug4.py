import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

def execute():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    camp_crit_service = client.get_service('CampaignCriterionService')

    category1_camps = ['Google-Sa-DSA-Global', 'Google-Sa-Testing-Global', 'Google-PMax-CP-Global']
    category1_words = [
        "openhands", "aider", "v0 by vercel", "bolt new", "openmanus", "openrouter",
        "n8n", "n8n community edition", "n8n cloud", "dify", "langgraph studio",
        "qwen 3.6 coder", "бесплатный api ключ deepseek",
        "pwa builder", "appmachine", "andromo", "create an app", "mobile app development",
        "https jsbin com", "run code online", "codepad", "pycharm community", "flask api", "main py"
    ]

    category2_camps = ['Google-PMax-Postman', 'Google-Sa-DSA-Global']
    category2_words = [
        "postman download", "postman online without login", "postman web app", 
        "thunder client free", "insomnia api testing download"
    ]

    # Map campaigns to their resource names
    camp_res_map = {}
    all_camps = list(set(category1_camps + category2_camps))
    
    camps_sql = ", ".join([f"'{c}'" for c in all_camps])
    q_camp = f"SELECT campaign.id, campaign.name, campaign.resource_name FROM campaign WHERE campaign.name IN ({camps_sql})"
    
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
        for row in batch.results:
            camp_res_map[row.campaign.name] = row.campaign.resource_name
            print(f"Found campaign: {row.campaign.name}")

    ops = []
    
    def build_neg_kw_ops(camp_names, words):
        for c in camp_names:
            if c not in camp_res_map:
                print(f"Warning: Campaign {c} not found, skipping...")
                continue
                
            camp_res = camp_res_map[c]
            for w in words:
                op = client.get_type("CampaignCriterionOperation")
                crit = op.create
                crit.campaign = camp_res
                crit.negative = True
                crit.keyword.text = w
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                ops.append(op)

    build_neg_kw_ops(category1_camps, category1_words)
    build_neg_kw_ops(category2_camps, category2_words)

    if not ops:
        print("No operations to perform.")
        return

    print(f"Adding {len(ops)} Campaign Negative Keywords...")
    req = client.get_type("MutateCampaignCriteriaRequest")
    req.customer_id = CUSTOMER_ID
    req.operations.extend(ops)
    req.partial_failure = True
    
    try:
        resp = camp_crit_service.mutate_campaign_criteria(request=req)
        if resp.partial_failure_error and resp.partial_failure_error.details:
            print("Partial failures occurred (likely duplicates or unsupported campaign types):")
            for err in resp.partial_failure_error.details:
                print(f"Error: {err}")
        else:
            print(f"Successfully added all negative keywords.")
    except GoogleAdsException as ex:
        print(f"GoogleAdsException occurred: {ex}")
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")

if __name__ == '__main__':
    execute()
