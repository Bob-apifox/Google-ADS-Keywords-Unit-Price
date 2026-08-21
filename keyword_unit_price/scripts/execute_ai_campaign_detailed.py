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

client = None
for i in range(3):
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        break
    except Exception as e:
        time.sleep(2)

if not client:
    print("Could not connect.")
    sys.exit(1)

def get_campaign_id(campaign_name):
    query = f"SELECT campaign.id FROM campaign WHERE campaign.name = '{campaign_name}' AND campaign.status = 'ENABLED'"
    ga_service = client.get_service("GoogleAdsService")
    for _ in range(5):
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    return row.campaign.id
        except:
            time.sleep(2)
    return None

def update_campaign_suffix(camp_id):
    camp_service = client.get_service("CampaignService")
    op = client.get_type("CampaignOperation")
    camp = op.update
    camp.resource_name = camp_service.campaign_path(CUSTOMER_ID, camp_id)
    camp.url_custom_parameters.clear() # clear existing to safely update suffix? No just set suffix
    camp.final_url_suffix = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"
    
    client.copy_from(op.update_mask, field_mask(None, camp._pb))
    
    for _ in range(5):
        try:
            camp_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
            print("✅ Updated Campaign Final URL Suffix")
            return
        except Exception as e:
            time.sleep(2)
    print("❌ Failed to update Campaign Suffix")

def get_or_create_ad_group(camp_id, ag_name, cpa_usd):
    query = f"SELECT ad_group.id FROM ad_group WHERE campaign.id = {camp_id} AND ad_group.name = '{ag_name}' AND ad_group.status != 'REMOVED'"
    ga_service = client.get_service("GoogleAdsService")
    
    existing_id = None
    for _ in range(3):
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    existing_id = row.ad_group.id
            break
        except:
            time.sleep(2)
            
    ag_service = client.get_service("AdGroupService")
    
    if existing_id:
        # Update CPA
        op = client.get_type("AdGroupOperation")
        ag = op.update
        ag.resource_name = ag_service.ad_group_path(CUSTOMER_ID, existing_id)
        ag.target_cpa_micros = int(cpa_usd * 1000000)
        client.copy_from(op.update_mask, field_mask(None, ag._pb))
        for _ in range(5):
            try:
                ag_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
                print(f"✅ Updated existing Ad Group: {ag_name} to CPA ${cpa_usd:.2f}")
                return existing_id
            except Exception:
                time.sleep(2)
        return existing_id
    else:
        # Create new
        op = client.get_type("AdGroupOperation")
        ag = op.create
        ag.campaign = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, camp_id)
        ag.name = ag_name
        ag.status = client.enums.AdGroupStatusEnum.ENABLED
        ag.target_cpa_micros = int(cpa_usd * 1000000)
        
        for _ in range(5):
            try:
                response = ag_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
                new_rn = response.results[0].resource_name
                new_id = new_rn.split('/')[-1]
                print(f"✅ Created new Ad Group: {ag_name} with CPA ${cpa_usd:.2f}")
                return new_id
            except Exception as e:
                time.sleep(2)
    return None

def create_ad_for_group(ag_id):
    # Only create for the new AI-Code-Generation
    ad_group_ad_service = client.get_service("AdGroupAdService")
    op = client.get_type("AdGroupAdOperation")
    ad_group_ad = op.create
    ad_group_ad.ad_group = client.get_service("AdGroupService").ad_group_path(CUSTOMER_ID, ag_id)
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    
    rsa = ad_group_ad.ad.responsive_search_ad
    
    headlines = ["AI API Design & Generation", "Auto-Generate OpenAPI Schema", "Apidog: AI API Developer Tool", "Generate API Docs Instantly", "Best AI API Testing Platform"]
    for hl in headlines:
        text_asset = client.get_type("AdTextAsset")
        text_asset.text = hl
        rsa.headlines.append(text_asset)
        
    descriptions = [
        "Generate your API documentation and mock servers instantly using our advanced AI tool.",
        "The most powerful AI-driven API design and testing platform for modern dev teams.",
        "Stop writing schemas manually. Let our AI copilot design and generate APIs for you."
    ]
    for d in descriptions:
        text_asset = client.get_type("AdTextAsset")
        text_asset.text = d
        rsa.descriptions.append(text_asset)
        
    ad_group_ad.ad.final_urls.append("https://apidog.com/ai-powered-workflow/")
    
    for _ in range(5):
        try:
            ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[op])
            print("✅ Created RSA Ad for AI-Code-Generation")
            return
        except Exception as e:
            time.sleep(2)

def add_keywords(ag_id, keywords):
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
            print(f"✅ Added {len(keywords)} expansion keywords")
            return
        except Exception:
            time.sleep(2)
    print(f"❌ Failed to add keywords")

def main():
    camp_id = get_campaign_id(CAMPAIGN_NAME)
    if not camp_id:
        print("Campaign not found.")
        return
        
    print("--- ⚙️ Updating Global Tracking ---")
    update_campaign_suffix(camp_id)
    
    groups_config = {
        "AI-Agent-Testing": {"cpa": 1.50, "kws": ['generative AI for QA', 'AI API testing', 'ai api test generator', 'api testing for ai agents', 'ai automated testing tools', 'ai qa automation', 'ai test case generator', 'automated api testing with ai', 'llm api testing', 'chatgpt api testing', 'ai software testing tools', 'api testing copilot', 'ai agent testing framework', 'test ai agents', 'evaluate llm agents', 'ai test automation platform']},
        "LLM-Benchmarking": {"cpa": 2.50, "kws": ['LLM API Comparison', 'DeepSeek vs GPT-4o API cost', 'best api ai', 'llm api pricing comparison', 'cheapest llm api', 'openai api alternatives', 'claude api vs openai api', 'llm api latency benchmark', 'fastest llm api', 'compare ai models api', 'llm api cost calculator', 'open source llm api hosting', 'best llm for api calls', 'llm api performance', 'ai model benchmark']},
        "MCP & AI Agents": {"cpa": 1.50, "kws": ['agentgpt', 'model context protocol mcp', 'mcp protocol api', 'build ai agents', 'ai agent framework', 'langchain api integration', 'llamaindex api tools', 'openai function calling api', 'ai agent tools api', 'model context protocol examples', 'ai agent api orchestration', 'auto gpt api', 'create custom ai agent', 'llm agent architecture']},
        "AI Infrastructure (MCP)": {"cpa": 1.50, "kws": ['mcp open source server', 'mcp deployment', 'open mcp architecture', 'host mcp server', 'ai infrastructure open source', 'deploy model context protocol', 'mcp server hosting', 'llm backend infrastructure', 'ai platform infrastructure']},
        "SSE & LLM Debugging": {"cpa": 1.50, "kws": ['sse streaming debugging', 'llm response streaming api', 'server sent events api', 'debug llm prompts', 'debug ai streams', 'test sse connections', 'llm stream testing tool', 'websocket vs sse for llm', 'chatgpt stream api testing']},
        "MCP-Testbench": {"cpa": 1.50, "kws": ['test mcp server', 'mcp testing tool', 'model context protocol validator', 'test ai agent framework', 'validate mcp integration', 'mcp client testing']},
        "AI-Code-Generation": {"cpa": 1.50, "kws": ['AI schema generator', 'ai schema', 'ai code generator for api', 'ai driven api development', 'ai api documentation generator', 'ai swagger generator', 'ai openapi generator', 'generate api with ai', 'ai backend generator', 'chatgpt code generator for api', 'ai json schema generator', 'ai api designer', 'llm code generation api', 'ai boilerplate generator', 'generate openapi spec with llm', 'swagger ai generator']}
    }
    
    print("\n--- 🚀 Ad Groups & Keywords Execution ---")
    for gname, data in groups_config.items():
        ag_id = get_or_create_ad_group(camp_id, gname, data["cpa"])
        if ag_id:
            add_keywords(ag_id, data["kws"])
            if gname == "AI-Code-Generation":
                create_ad_for_group(ag_id)

    print("\n🎉 AI Campaign Extreme Expansion completed successfully!")

if __name__ == "__main__":
    main()
