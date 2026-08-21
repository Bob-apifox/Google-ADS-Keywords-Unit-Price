import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient
from google.api_core.protobuf_helpers import field_mask

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"
CAMPAIGN_NAME = "Google-Sa-Solutions-AI-LLM-Global"

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)

def get_existing_id(ag_name):
    ga_service = client.get_service("GoogleAdsService")
    query = f"SELECT ad_group.id FROM ad_group WHERE campaign.name = '{CAMPAIGN_NAME}' AND ad_group.name = '{ag_name}' AND ad_group.status != 'REMOVED'"
    for _ in range(5):
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    return row.ad_group.id
        except:
            time.sleep(2)
    return None

def update_cpa(ag_id, cpa_usd):
    ag_service = client.get_service("AdGroupService")
    op = client.get_type("AdGroupOperation")
    ag = op.update
    ag.resource_name = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
    ag.target_cpa_micros = int(cpa_usd * 1000000)
    client.copy_from(op.update_mask, field_mask(None, ag._pb))
    for _ in range(5):
        try:
            ag_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
            print(f"✅ CPA Updated")
            return
        except:
            time.sleep(2)

def add_kws(ag_id, keywords):
    ag_crit_service = client.get_service("AdGroupCriterionService")
    operations = []
    for kw in keywords:
        op = client.get_type("AdGroupCriterionOperation")
        crit = op.create
        crit.ad_group = client.get_service("AdGroupService").ad_group_path(CUSTOMER_ID, ag_id)
        crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        crit.keyword.text = kw
        crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        operations.append(op)
    for _ in range(5):
        try:
            ag_crit_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=operations)
            print(f"✅ Added {len(keywords)} kws")
            return
        except:
            time.sleep(2)

def main():
    print("Patching missed API calls due to proxy...")
    # 1. Update CPA for LLM-Benchmarking
    ag1 = get_existing_id("LLM-Benchmarking")
    if ag1: update_cpa(ag1, 2.50)
    
    # 2. Update CPA for MCP & AI Agents
    ag2 = get_existing_id("MCP & AI Agents")
    if ag2: update_cpa(ag2, 1.50)
    
    # 3. Fix AI Infrastructure (MCP) which was skipped entirely
    ag3 = get_existing_id("AI Infrastructure (MCP)")
    if ag3:
        update_cpa(ag3, 1.50)
        kws = ['mcp open source server', 'mcp deployment', 'open mcp architecture', 'host mcp server', 'ai infrastructure open source', 'deploy model context protocol', 'mcp server hosting', 'llm backend infrastructure', 'ai platform infrastructure']
        add_kws(ag3, kws)
    print("Done patching.")

if __name__ == "__main__":
    main()
