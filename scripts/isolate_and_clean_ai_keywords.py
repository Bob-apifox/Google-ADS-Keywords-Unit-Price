import os
import sys
import urllib3
from google.ads.googleads.client import GoogleAdsClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ["GOOGLE_ADS_USE_REST"] = "true"
sys.stdout.reconfigure(encoding='utf-8')

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    agc_service = client.get_service("AdGroupCriterionService")
    
    query = """
        SELECT
            campaign.name,
            ad_group_criterion.resource_name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.status
        FROM keyword_view
        WHERE ad_group_criterion.status = 'ENABLED'
    """
    
    stream = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    ai_terms = ['ai', 'llm', 'gpt', 'cursor', 'claude', 'copilot', 'deepseek', 'qwen', 'ollama', 'openhands', 'aider', 'v0', 'bolt']
    
    ops = []
    for row in stream:
        cname = row.campaign.name
        res_name = row.ad_group_criterion.resource_name
        kw = row.ad_group_criterion.keyword.text.lower()
        
        # Skip AI-LLM targeted campaign
        if "AI-LLM" in cname:
            continue
            
        words = kw.split()
        contains_ai = any(t in words or f" {t} " in f" {kw} " or kw.startswith(f"{t} ") or kw.endswith(f" {t}") for t in ai_terms)
        
        if contains_ai:
            op = client.get_type("AdGroupCriterionOperation")
            criterion = op.update
            criterion.resource_name = res_name
            criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
            op.update_mask.paths.append("status")
            ops.append(op)
            
    print(f"Prepared {len(ops)} operations to PAUSE leaking AI keywords in non-AI campaigns.")
    
    if ops:
        chunk_size = 1000
        for i in range(0, len(ops), chunk_size):
            chunk = ops[i:i+chunk_size]
            req = client.get_type("MutateAdGroupCriteriaRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(chunk)
            req.partial_failure = True
            res = agc_service.mutate_ad_group_criteria(request=req)
            print(f"Chunk {i//chunk_size + 1}: Mutated {len(chunk)} criteria.")

    print("✅ AI Keyword Isolation & Cleaning Completed Successfully!")

if __name__ == '__main__':
    main()
