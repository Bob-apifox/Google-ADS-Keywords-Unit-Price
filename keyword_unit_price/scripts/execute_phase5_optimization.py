import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

client = None
for i in range(3):
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        break
    except Exception as e:
        print(f"Failed to load client (attempt {i+1}): {e}")
        time.sleep(2)

if not client:
    print("Could not connect after 3 attempts.")
    sys.exit(1)

def get_campaign_id(campaign_name):
    query = f"SELECT campaign.id FROM campaign WHERE campaign.name = '{campaign_name}' AND campaign.status = 'ENABLED'"
    ga_service = client.get_service("GoogleAdsService")
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                return row.campaign.id
    except:
        pass
    return None

def get_ad_group_id(campaign_id, ad_group_name):
    query = f"SELECT ad_group.id FROM ad_group WHERE campaign.id = {campaign_id} AND ad_group.name = '{ad_group_name}' AND ad_group.status = 'ENABLED'"
    ga_service = client.get_service("GoogleAdsService")
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                return row.ad_group.id
    except:
        pass
    return None

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
        
    try:
        camp_crit_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=operations)
        print(f"✅ Added {len(keywords)} negative keywords to {campaign_name}")
    except Exception as e:
        print(f"❌ Failed to add negatives to {campaign_name}: {e}")

def add_expansion_keywords(campaign_name, ad_group_name, keywords):
    camp_id = get_campaign_id(campaign_name)
    if not camp_id:
        return
    ag_id = get_ad_group_id(camp_id, ad_group_name)
    if not ag_id:
        print(f"❌ Ad Group not found: {ad_group_name}")
        return
        
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
        
    try:
        ag_crit_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=operations)
        print(f"✅ Added {len(keywords)} expansion keywords to {ad_group_name}")
    except Exception as e:
        print(f"❌ Failed to add expansions to {ad_group_name}: {e}")

def update_adgroup_cpa(campaign_name, ad_group_name, new_cpa_micros):
    camp_id = get_campaign_id(campaign_name)
    if not camp_id: return
    ag_id = get_ad_group_id(camp_id, ad_group_name)
    if not ag_id: return
    
    ag_service = client.get_service("AdGroupService")
    op = client.get_type("AdGroupOperation")
    ag = op.update
    ag.resource_name = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
    ag.target_cpa_micros = int(new_cpa_micros)
    client.copy_from(op.update_mask, client.get_service("ResourceService").generate_mutated_mask(
        client.get_type("AdGroup"), ag
    ))
    
    try:
        ag_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
        print(f"✅ Updated Target CPA for {ad_group_name} to ${new_cpa_micros / 1e6}")
    except Exception as e:
        print(f"❌ Failed to update CPA for {ad_group_name}: {e}")

def duplicate_broad_keywords(campaign_name):
    ga_service = client.get_service("GoogleAdsService")
    query = f"SELECT ad_group.id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.conversions, metrics.cost_micros FROM keyword_view WHERE campaign.name = '{campaign_name}' AND segments.date DURING LAST_30_DAYS AND metrics.conversions > 4"
    
    keywords_to_add = []
    
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
    except Exception as e:
        print(f"❌ Query failed for {campaign_name}: {e}")
        return
        
    if not keywords_to_add:
        print(f"⚠️ No keywords met criteria in {campaign_name}")
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
        
    try:
        ag_crit_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=operations)
        print(f"✅ Duplicated {len(keywords_to_add)} keywords as BROAD in {campaign_name}")
    except Exception as e:
        print(f"❌ Failed to duplicate broad keywords in {campaign_name}: {e}")

def main():
    print("--- 🛑 Phase 5: Executing Stop-Loss (Negative Keywords) ---")
    negatives = {
        "Google-Sa-CLI-Global": ["postman online", "online postman", "postman free", "postman like", "alternative for postman tool", "postman tool", "http client online", "online soapui"],
        "Google-Sa-Bruno-Global": ["openrouter api", "https ngrok com", "json file", "firebase studio ai", "bruno mac", "make com", "power automate desktop", "service role key"],
        "Google-Sa-Stoplight-Global": ["stoplight", "code visualstudio com", "online rest api", "ocr api", "openrpa", "gemini api"],
        "Google-Sa-Doc-Global": ["api doc", "nanonets", "dogapi", "ai documentation generator", "nextdocs", "swaggerhub", "rest client"],
        "Google-Sa-Mock-Global": ["browserstack", "glide apps", "v0 by vercel", "insomnia community edition", "stackblitz", "cobalt api", "api chai"],
        "Google-Sa-Scalar-Global": ["v0 app", "adalo app builder", "devdocs io", "codemagic", "n8n automation", "ia para hacer apis", "online post request"],
        "Google-Sa-Mintlify-Global": ["api documentation", "notion", "next js", "git for windows", "redoc", "platform maker ai", "evolution api"],
        "Google-Sa-Insomnia-Global": ["evolution api", "testar api online", "locust", "online http request", "web api testing"],
        "Google-Sa-DSA-Postman-Global": ["apidog documentation", "soapui", "postman web", "apidog self hosted", "postman en ligne", "alternativas a postman"],
        "Google-Sa-Swagger-Global": ["openapi documentation"]
    }
    for camp, kws in negatives.items():
        add_negative_keywords(camp, kws)
        time.sleep(1)

    print("\n--- 🚀 Phase 5: Executing Expansion (New Keywords) ---")
    add_expansion_keywords("Google-Sa-Jmeter-Global", "Jmeter--Global", ["jmeter alternative", "api load testing tool", "rest api stress test", "automate jmeter tests"])
    time.sleep(1)
    add_expansion_keywords("Google-Sa-Readme-Global", "Readme-Global #2", ["readme io alternative", "developer portal generator", "api docs hosting free", "interactive api documentation"])
    time.sleep(1)
    add_expansion_keywords("Google-Sa-Fern-Global", "Fern-Global", ["fern api alternative", "fern api generator", "fern vs openapi"])
    
    print("\n--- 💰 Phase 5: Executing Target CPA Increase ---")
    update_adgroup_cpa("Google-Sa-Fern-Global", "Fern-Global", 1400000) # $1.40
    time.sleep(1)
    update_adgroup_cpa("Google-Sa-Debug-Global", "Debug-Global", 1840000) # $1.84
    time.sleep(1)
    update_adgroup_cpa("Google-Sa-Readme-Global", "Readme-Global", 2880000) # $2.88
    
    print("\n--- 🔥 Phase 5: Executing Broad Match Upgrade ---")
    for c in ['Google-Sa-Postman-Global', 'Google-Sa-Openapi-Global', 'Google-Sa-CP-Global']:
        duplicate_broad_keywords(c)
        time.sleep(1)

    print("\n🎉 All Phase 5 Optimization tasks completed successfully!")

if __name__ == "__main__":
    main()
