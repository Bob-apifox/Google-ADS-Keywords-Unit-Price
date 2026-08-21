import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")
campaign_criterion_service = client.get_service("CampaignCriterionService")

app_builder_negatives = ["create app", "make app", "app generator", "app builder", "app developer", "app development", "app creation", "build an app", "app design", "glide", "bubble io", "appsheet", "adalo", "appgyver", "power apps", "nocobase", "natively dev"]
ai_generator_negatives = ["v0 dev", "v0 by vercel", "bolt new", "lovable", "magic loops", "codeium", "cursor ide", "tabnine", "aider", "openhands", "windsurf"]
unrelated_framework_negatives = ["node js", "pycharm", "idle shell", "tomcat", "flask", "cordova", "phonegap", "netlify drop"]

campaign_negatives_map = {
    "Google-Sa-API Editor-Global": app_builder_negatives,
    "Google-Sa-Design-Global": app_builder_negatives,
    "Google-Sa-Bruno-Global": app_builder_negatives + ai_generator_negatives,
    "Google-Sa-Mintlify-Global": app_builder_negatives + ai_generator_negatives,
    "Google-Sa-Stoplight-Global": app_builder_negatives,
    "Google-Sa-Readme-Global": app_builder_negatives,
    "Google-Sa-Bump.sh-Global": app_builder_negatives + ai_generator_negatives,
    "Google-Sa-Solutions-Unified-API-Global": app_builder_negatives,
    "Google-Sa-Annual Planning & New Trends-26": app_builder_negatives,
    
    "Google-Sa-Expansion-Horizon-2026": ai_generator_negatives,
    "Google-Sa-Openapi-Global": ai_generator_negatives + unrelated_framework_negatives,
    "Google-Sa-Function-Global": ai_generator_negatives,
    "Google-Sa-Debug-Global": ai_generator_negatives,
    
    "Google-Sa-CP-Global": unrelated_framework_negatives,
    "Google-Sa-Jmeter-Global": unrelated_framework_negatives
}

query = "SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = 'ENABLED'"
response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
campaign_id_map = {}
for row in response:
    campaign_id_map[row.campaign.name] = row.campaign.id

operations = []
for c_name, words in campaign_negatives_map.items():
    if c_name in campaign_id_map:
        c_id = campaign_id_map[c_name]
        c_resource_name = ga_service.campaign_path(CUSTOMER_ID, c_id)
        
        unique_words = list(set(words))
        for word in unique_words:
            op = client.get_type("CampaignCriterionOperation")
            criterion = op.create
            criterion.campaign = c_resource_name
            criterion.negative = True
            
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            criterion.keyword.text = word
            
            operations.append(op)
    else:
        print(f"Warning: Campaign '{c_name}' not found or not enabled.")

print(f"Total negative keywords to add: {len(operations)}")

batch_size = 1000
for i in range(0, len(operations), batch_size):
    batch = operations[i:i+batch_size]
    try:
        response = campaign_criterion_service.mutate_campaign_criteria(
            customer_id=CUSTOMER_ID, operations=batch
        )
        print(f"Successfully added {len(response.results)} negative keywords.")
    except Exception as e:
        print(f"Error adding negative keywords: {e}")

print("Done.")
