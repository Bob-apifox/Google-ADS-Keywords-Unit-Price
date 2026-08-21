import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service('GoogleAdsService')
campaign_budget_service = client.get_service('CampaignBudgetService')
ad_group_service = client.get_service('AdGroupService')
campaign_criterion_service = client.get_service('CampaignCriterionService')

# Targets
budget_decrease_50 = ['Google-Sa-API Editor-Global', 'Google-Sa-Mock-Global', 'Google-Sa-Bruno-Global', 'Google-Sa-Doc-Global']
budget_increase_50 = ['Google-Sa-CP-Global', 'Google-Sa-Category-Competitor-Global', 'Google-Sa-The "Great Migration"-26', 'Google-Sa-Function-Global']
budget_increase_30 = ['Google-Sa-Postman-Global', 'Google-Sa-DSA-Postman-Global']

ad_groups_to_pause = {
    'Google-Sa-Solutions-API-First-Global': ['Ad group 1', 'JSON Schema Tooling'],
    'Google-Sa-Solutions-Multi-Protocol-Global': ['Advanced Mocking', 'Ad group 1', 'Unified Platform'],
    'Google-Sa-API Editor-Global': ['No-Code & Builder-Global', 'api-document-Global'],
    'Google-Sa-Bruno-Global': ['Insomnia--Global', 'Doc-CP-Global', 'Doc-Global'],
    'Google-Sa-Mintlify-Global': ['Doc-Global', 'Insomnia--Global', 'Doc-CP-Global', 'api-document-Global'],
    'Google-Sa-Doc-Global': ['Doc-CP-Global', 'Swagger--Global', 'Stoplight--Global'],
    'Google-Sa-Readme-Global': ['Swagger--Global', 'Doc-CP-Global', 'api-document-Global', 'Insomnia--Global'],
    'Google-Sa-CLI-Global': ['Ad group 1', 'CLI-CICD-Integration'],
    'Google-Sa-Fern-Global': ['Swagger--Global', 'Insomnia--Global', 'Readme-Global #2', 'api-document-Global'],
    'Google-Sa-Annual Planning & New Trends-26': ['Direct Alternatives-26', 'postman-DSA'],
    'Google-Sa-Scalar-Global': ['Readme-Global #2', 'Doc-CP-Global', 'Swagger--Global', 'Insomnia--Global'],
    'Google-Sa-Openapi-Global': ['OpenAPI-Smart-Editor-Global', 'Stoplight--Global', 'OpenAPI-Visual-Editor--Global'],
    'Google-Sa-Stoplight-Global': ['Insomnia--Global', 'Doc-Global'],
    'Google-Sa-SpecFirst-Global': ['Git-Native-API', 'Spec-First-Methodology', 'Ad group 1'],
    'Google-Sa-RapidAPI-Global': ['Swagger--Global', 'Insomnia--Global', 'Doc-Global', 'Doc-CP-Global'],
    'Google-Sa-Swagger-Global': ['Swagger offline--Global', 'Openapi-Global']
}

negative_kws = {
    'Google-Sa-Solutions-API-First-Global': ['code generator ai', 'post api call', 'dev tools api', 'testar api'],
    'Google-Sa-Solutions-Multi-Protocol-Global': ['online api tester', 'category debuggers json with comments', 'fiddler classic', 'web api testing tool', 'testar webhook', 'supabase com'],
    'Google-Sa-MCP-Infrastructure': ['api dog mcp'],
    'Google-Sa-API Editor-Global': ['app creation software', 'app design_guidelines json', 'spck editor', 'openapi designer', 'cordova', 'software development', 'notion', 'vscode online', 'the net framework', 'airtable app'],
    'Google-Sa-Mock-Global': ['firebase studio', 'json', 'api mock', 'dashscope', 'anyapi', 'budibase', 'app backend server py', 'firebase firestore', 'composio', 'cordova cli'],
    'Google-Sa-Bruno-Global': ['nocodeapi', 'buildmyagent io', 'nocobase', 'testobject', 'deepseek v4 pro api', 'app making software', 'advanced rest client', 'www odoo com website', 'appgyver sap build apps', 'web app url'],
    'Google-Sa-Mintlify-Global': ['bolt new ai', 'lovable', 'online api test', '21st dev', 'docsumo', 'community edition ce', 'webstorm intellij idea', 'markdown', 'ide', 'bubble no code'],
    'Google-Sa-Doc-Global': ['api documentation platforms', 'api test tools', 'testar api', 'typescript', 'doclingo ai', 'glide', 'sharayeh ai document formatter', 'ai for document creation', 'openapi generator'],
    'Google-Sa-Readme-Global': ['glide apps', 'windsurf ai', 'app coding website', 'api checker', 'appy pie', 'app creator', 'coding', 'asyncapi online', 'deepseek api', 'online api caller'],
    'Google-Sa-CLI-Global': ['postman free alternative', 'app like postman', 'postman alternate'],
    'Google-Sa-Annual Planning & New Trends-26': ['magic loops', 'netlify drop', 'how we make app', 'emergent sh', 'bolt ai', 'where can i create an app', 'ai code', 'black box ai'],
    'Google-Sa-Scalar-Global': ['online api test'],
    'Google-Sa-Openapi-Global': ['no code', 'code editing redefined', 'فيجوال ستوديو كود', 'codeium', 'godot engine', 'ai app builder', 'v s code', 'stackblitz', 'lama coder', 'manus ai builder'],
    'Google-Sa-Stoplight-Global': ['api documentation tool', 'opencode', 'appy pie', 'best tool for api testing', 'soap client online', 'api calls online', 'firebase', 'jetbrains', 'google vision api', 'microsoft power apps'],
    'Google-Sa-SpecFirst-Global': ['postman download', 'download apis', 'bruno api testing', 'postman free alternatives', 'swagger editor', 'api download', 'free mock api', 'alternative swagger ui', 'test api online free', 'backend coding ai'],
    'Google-Sa-RapidAPI-Global': ['api request online', 'supabase com', 'i want to make software', 'software programing', 'oauth2 proxy', 'qodo', 'adalo app'],
    'Google-Sa-Swagger-Global': ['api documenter', 'insomnia api documentation', 'openapi designer']
}

budget_ops = {}
ad_group_ops = []
campaign_ids = {}

print("Fetching campaign budgets...")
query_campaign = '''
    SELECT 
        campaign.id, campaign.name, campaign_budget.id, campaign_budget.amount_micros
    FROM campaign
    WHERE campaign.status = 'ENABLED'
'''
stream_campaign = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_campaign)

for batch in stream_campaign:
    for row in batch.results:
        c_name = row.campaign.name
        c_id = row.campaign.id
        b_id = row.campaign_budget.id
        b_amount = row.campaign_budget.amount_micros
        
        campaign_ids[c_name] = c_id
        
        if b_id not in budget_ops:
            new_amount = b_amount
            if c_name in budget_decrease_50:
                new_amount = int(b_amount * 0.5)
            elif c_name in budget_increase_50:
                new_amount = int(b_amount * 1.5)
            elif c_name in budget_increase_30:
                new_amount = int(b_amount * 1.3)
            
            if new_amount != b_amount:
                op = client.get_type("CampaignBudgetOperation")
                budget = op.update
                budget.resource_name = campaign_budget_service.campaign_budget_path(CUSTOMER_ID, b_id)
                budget.amount_micros = new_amount
                client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, budget._pb))
                budget_ops[b_id] = op

print("Fetching active ad groups...")
query_ag = '''
    SELECT 
        campaign.name, ad_group.id, ad_group.name, ad_group.status
    FROM ad_group
    WHERE campaign.status = 'ENABLED'
'''
stream_ag = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_ag)

for batch in stream_ag:
    for row in batch.results:
        c_name = row.campaign.name
        ag_name = row.ad_group.name
        ag_id = row.ad_group.id
        ag_status = row.ad_group.status.name
        
        if c_name in ad_groups_to_pause and ag_name in ad_groups_to_pause[c_name] and ag_status == 'ENABLED':
            op = client.get_type("AdGroupOperation")
            ag = op.update
            ag.resource_name = ad_group_service.ad_group_path(CUSTOMER_ID, ag_id)
            ag.status = client.enums.AdGroupStatusEnum.PAUSED
            client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, ag._pb))
            ad_group_ops.append(op)

# 3. Negative Keywords
criterion_ops = []
for c_name, kws in negative_kws.items():
    if c_name in campaign_ids:
        c_id = campaign_ids[c_name]
        for kw in kws:
            op = client.get_type("CampaignCriterionOperation")
            criterion = op.create
            criterion.campaign = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, c_id)
            criterion.negative = True
            criterion.keyword.text = kw
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            criterion_ops.append(op)

print(f"Prepared {len(budget_ops)} budget updates.")
print(f"Prepared {len(ad_group_ops)} ad group pauses.")
print(f"Prepared {len(criterion_ops)} negative keywords.")

print("Executing Budget Updates...")
if budget_ops:
    try:
        response = campaign_budget_service.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=list(budget_ops.values()))
        print(f"Success: Updated {len(response.results)} budgets.")
    except Exception as e:
        print(f"Budget Error: {e}")

print("Executing Ad Group Pauses...")
if ad_group_ops:
    try:
        response = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=ad_group_ops)
        print(f"Success: Paused {len(response.results)} ad groups.")
    except Exception as e:
        print(f"Ad Group Error: {e}")

print("Executing Negative Keywords Injection...")
if criterion_ops:
    try:
        response = campaign_criterion_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=criterion_ops)
        print(f"Success: Added {len(response.results)} negative keywords.")
    except Exception as e:
        print(f"Negative Keyword Error: {e}")

print("DONE.")
