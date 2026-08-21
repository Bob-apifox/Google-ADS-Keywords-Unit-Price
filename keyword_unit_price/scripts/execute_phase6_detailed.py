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

def get_first_ad_group_id_and_cpa(campaign_id):
    query = f"SELECT ad_group.id, ad_group.target_cpa_micros FROM ad_group WHERE campaign.id = {campaign_id} AND ad_group.status = 'ENABLED' LIMIT 1"
    ga_service = client.get_service("GoogleAdsService")
    for _ in range(5):
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    return row.ad_group.id, getattr(row.ad_group, 'target_cpa_micros', None)
        except:
            time.sleep(2)
    return None, None

def add_negative_keywords(campaign_name, keywords):
    camp_id = get_campaign_id(campaign_name)
    if not camp_id:
        print(f"❌ Campaign not found: {campaign_name}")
        return
        
    camp_crit_service = client.get_service("CampaignCriterionService")
    operations = []
    
    for kw in keywords:
        op = client.get_type("CampaignCriterionOperation")
        crit = op.create
        crit.campaign = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, camp_id)
        crit.negative = True
        crit.keyword.text = kw
        crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        operations.append(op)
        
    for _ in range(5):
        try:
            camp_crit_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=operations)
            print(f"✅ Added {len(keywords)} negatives to {campaign_name}")
            return
        except Exception:
            time.sleep(2)
    print(f"❌ Failed to add negatives to {campaign_name}")

def add_expansion_keywords(campaign_name, keywords):
    camp_id = get_campaign_id(campaign_name)
    if not camp_id: return
    ag_id, _ = get_first_ad_group_id_and_cpa(camp_id)
    if not ag_id: return
        
    ag_crit_service = client.get_service("AdGroupCriterionService")
    operations = []
    
    for kw in keywords:
        op = client.get_type("AdGroupCriterionOperation")
        crit = op.create
        crit.ad_group = client.get_service("AdGroupService").ad_group_path(CUSTOMER_ID, ag_id)
        crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        crit.keyword.text = kw
        crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        operations.append(op)
        
    for _ in range(5):
        try:
            ag_crit_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=operations)
            print(f"✅ Added {len(keywords)} expansions to {campaign_name}")
            return
        except Exception:
            time.sleep(2)

def update_adgroup_cpa_dynamic(campaign_name):
    camp_id = get_campaign_id(campaign_name)
    if not camp_id: return
    ag_id, current_cpa = get_first_ad_group_id_and_cpa(camp_id)
    if not ag_id: return
    
    if not current_cpa or current_cpa == 0:
        print(f"⚠️ No Target CPA found for {campaign_name} (might be maximize conversions without target)")
        return
        
    new_cpa_micros = int(current_cpa * 1.15)
    
    ag_service = client.get_service("AdGroupService")
    op = client.get_type("AdGroupOperation")
    ag = op.update
    ag.resource_name = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
    ag.target_cpa_micros = new_cpa_micros
    
    client.copy_from(op.update_mask, field_mask(None, ag._pb))
    
    for _ in range(5):
        try:
            ag_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
            print(f"✅ Updated CPA for {campaign_name} from ${current_cpa/1e6:.2f} to ${new_cpa_micros/1e6:.2f}")
            return
        except Exception:
            time.sleep(2)
    print(f"❌ Failed to update CPA for {campaign_name}")

def duplicate_broad_keywords(campaign_name):
    ga_service = client.get_service("GoogleAdsService")
    query = f"SELECT ad_group.id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.conversions, metrics.cost_micros FROM keyword_view WHERE campaign.name = '{campaign_name}' AND segments.date DURING LAST_30_DAYS AND metrics.conversions > 4"
    
    keywords_to_add = []
    
    for _ in range(3):
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    cost = row.metrics.cost_micros / 1e6
                    convs = row.metrics.conversions
                    cpa = cost / convs if convs > 0 else 0
                    if cpa < 4.0 and row.ad_group_criterion.keyword.match_type.name != 'BROAD':
                        keywords_to_add.append({
                            "ag_id": row.ad_group.id,
                            "text": row.ad_group_criterion.keyword.text
                        })
            break
        except:
            time.sleep(2)
            
    if not keywords_to_add:
        print(f"⚠️ No keywords met broad-match criteria in {campaign_name}")
        return
        
    ag_crit_service = client.get_service("AdGroupCriterionService")
    operations = []
    for kw in keywords_to_add:
        op = client.get_type("AdGroupCriterionOperation")
        crit = op.create
        crit.ad_group = client.get_service("AdGroupService").ad_group_path(CUSTOMER_ID, kw['ag_id'])
        crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        crit.keyword.text = kw['text']
        crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        operations.append(op)
        
    for _ in range(5):
        try:
            ag_crit_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=operations)
            print(f"✅ Duplicated {len(keywords_to_add)} keywords as BROAD in {campaign_name}")
            return
        except Exception:
            time.sleep(2)
    print(f"❌ Failed to duplicate broad keywords in {campaign_name}")

def main():
    print("--- 🛑 Phase 6: Injecting Negatives ---")
    negs = {
        "Google-Sa-CLI-Global": ['postman online', 'online postman', 'postman tool', 'postman online free', 'postman web', 'postman free', 'postman web free', 'postman like'],
        "Google-Sa-Stoplight-Global": ['openrpa', 'hugging face inference api', 'apphive', 'gemini api', 'openrouter api', 'codegpt'],
        "Google-Sa-Mock-Global": ['browserstack', 'glide apps', 'cobalt api', 'insomnia community edition', 'restler', 'stackblitz', 'api chai', 'apollo client', 'src app tsx', 'backend'],
        "Google-Sa-Func-MultiProtocol-Global": ['graphql playground online', 'grpc ui client', 'graphql client online', 'online websocket tester', 'graphql playground download', 'online graphql client', 'studio apollographql', 'grpc client'],
        "Google-Sa-Bruno-Global": ['openrouter api', 'bruno api tool', 'https modeler cloud camunda io', 'hugging face inference api', 'https ngrok com', 'json file', 'firebase studio ai', 'bruno mac', 'make com', 'service role key'],
        "Google-Sa-API Editor-Global": ['retool com api generator', 'traycer', 'rocket com', 'openapi 3.1', 'crear programa'],
        "Google-Sa-Swagger-Global": ['openapi documentation'],
        "Google-Sa-Enterprise-Global": ['mockoon', 'cohere api'],
        "Google-Sa-Comp-HeavyQA-Global": ['soapui alternative'],
        "Google-Sa-Insomnia-Global": ['evolution api', 'testar api online', 'locust', 'insomnia app']
    }
    for c, kws in negs.items():
        add_negative_keywords(c, kws)

    print("\n--- 🚀 Phase 6: Injecting Expansion Keywords ---")
    exps = {
        "Google-Sa-Design-Global": ['api design alternative', 'visual api designer', 'best api design tools'],
        "Google-Sa-Testing-Global": ['api testing automation tool', 'api test automation free', 'automated api testing platform'],
        "Google-Sa-MCP-Infrastructure": ['model context protocol mcp', 'mcp protocol api', 'open mcp server'],
        "Google-Sa-Comp-VSCode-Global": ['vscode api client', 'thunder client alternative', 'rest client extension alternative']
    }
    for c, kws in exps.items():
        add_expansion_keywords(c, kws)

    print("\n--- 💰 Phase 6: Target CPA Increase ---")
    for c in exps.keys():
        update_adgroup_cpa_dynamic(c)
        
    print("\n--- 🔥 Phase 6: Broad Match Upgrade ---")
    for c in ['Google-Sa-Postman-Global', 'Google-Sa-CP-Global', 'Google-Sa-Jmeter-Global', 'Google-Sa-Scalar-Global', 'Google-Sa-Hoppscotch-Global']:
        duplicate_broad_keywords(c)

    print("\n🎉 Phase 6 Optimization script completed successfully!")

if __name__ == "__main__":
    main()
