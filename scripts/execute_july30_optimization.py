import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
campaign_budget_service = client.get_service('CampaignBudgetService')
ad_group_criterion_service = client.get_service('AdGroupCriterionService')
campaign_criterion_service = client.get_service('CampaignCriterionService')
customer_id = '9496728294'

print("=== 1. Updating Budgets ===")
budgets = {
    'Google-Sa-Testing-Global': 93.50,
    'Google-Sa-Func-CICD-Global': 33.00
}

query = """
    SELECT campaign.id, campaign.name, campaign_budget.resource_name
    FROM campaign
    WHERE campaign.status = 'ENABLED'
"""
response = ga_service.search(customer_id=customer_id, query=query)
budget_ops = []
campaign_ids = {}

for row in response:
    name = row.campaign.name
    campaign_ids[name] = str(row.campaign.id)
    if name in budgets:
        budget_operation = client.get_type("CampaignBudgetOperation")
        budget_update = budget_operation.update
        budget_update.resource_name = row.campaign_budget.resource_name
        budget_update.amount_micros = int(budgets[name] * 1000000)
        client.copy_from(budget_operation.update_mask, protobuf_helpers.field_mask(None, budget_update._pb))
        budget_ops.append(budget_operation)

if budget_ops:
    campaign_budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=budget_ops)
    print("Budgets updated successfully.")

print("\n=== 2. Adding Broad Match Keywords ===")
# Ad groups that need broad match breaking
ad_groups_to_broaden = [
    'ReadyAPI-Target', 
    'Terminal-Native-Clients', 
    'Stoplight Alternative--Global',
    'Design-First Workflow'
]

# Get the ad group IDs and their current keywords
query_ag = f"""
    SELECT ad_group.id, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
    FROM ad_group_criterion
    WHERE ad_group.name IN ({', '.join([f"'{ag}'" for ag in ad_groups_to_broaden])})
    AND ad_group.status = 'ENABLED'
    AND ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.status = 'ENABLED'
"""
ag_response = ga_service.search(customer_id=customer_id, query=query_ag)

adgroup_kws = {}
for row in ag_response:
    ag_id = str(row.ad_group.id)
    ag_name = row.ad_group.name
    kw_text = row.ad_group_criterion.keyword.text
    kw_match = row.ad_group_criterion.keyword.match_type.name
    if ag_name not in adgroup_kws:
        adgroup_kws[ag_name] = {'id': ag_id, 'texts': set(), 'broad_exists': set()}
    if kw_match == 'BROAD':
        adgroup_kws[ag_name]['broad_exists'].add(kw_text)
    adgroup_kws[ag_name]['texts'].add(kw_text)

kw_ops = []
for ag_name, data in adgroup_kws.items():
    for text in data['texts']:
        if text not in data['broad_exists']:
            op = client.get_type("AdGroupCriterionOperation")
            op.create.ad_group = client.get_service("AdGroupService").ad_group_path(customer_id, data['id'])
            op.create.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            op.create.keyword.text = text
            op.create.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
            kw_ops.append(op)
            print(f"Prepared BROAD keyword '{text}' for {ag_name}")

if kw_ops:
    ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=kw_ops)
    print("Broad match keywords added successfully.")

print("\n=== 3. Adding Negative Keywords ===")
negatives = {
    'Google-Sa-Bruno-Global': ['pwa builder', 'app building software', 'progressive web app pwa', 'pwa', 'app creator', 'flutter dev', 'application maker', 'dummyjson'],
    'Google-Sa-Func-CICD-Global': ['github codespaces', 'github pages', 'https github com', 'github copilot free'],
    'Google-Sa-Func-MultiProtocol-Global': ['websocket', 'websockets'],
    'Google-Sa-Insomnia-Global': ['pocketbase', 'https ngrok com', 'openmanus'],
    'Google-Sa-Testing-Global': ['otp bypass mitigation owasp', 'bwapp', 'canarytokens'],
    'Google-Sa-Hoppscotch-Global': ['دانلود hoppscotch'],
    'Google-Sa-MCP-Infrastructure': ['claude code', 'codeium', 'dnspy', 'claude mcp', 'code visualstudio com', 'google gemini code assist', 'autogpt', 'mcp client'],
    'Google-Sa-Doc-Global': ['mocky', 'fastreport designer'],
    'Google-Sa-Stoplight-Global': ['openrouter', 'js bin', 'application x www form urlencoded', 'laragon', 'ui vision rpa extension'],
    'Google-Sa-Mintlify-Global': ['mintlify ai', 'header accept application json'],
    'Google-Sa-Mock-Global': ['web app maker', 'flask api', 'kiwi tcms', 'thunderclient', 'bitbar', 'flutterflow com', 'smartbear bitbar'],
    'Google-Sa-Design-Global': ['generator pages dev', 'pwa builder'],
    'Google-Sa-Function-Global': ['rest client extension'],
    'Google-Sa-Scalar-Global': ['n8n community edition', 'n8n'],
    'Google-Sa-Fern-Global': ['main py', 'appmachine', 'app generator ai', 'andromo', 'coding apps for pc', 'acode windows'],
    'Google-Sa-Annual Planning & New Trends-26': ['build app', 'react next js', 'idea to app', 'apps create', 'ao dev', 'webviewgold', 'web apps', 'best ai for build app'],
    'Google-Sa-Postman-Global': ['postma'],
    'Google-Sa-Openapi-Global': ['google studio', 'www odoo com website', 'open code ai', 'galileo ai']
}

neg_ops = []
for camp_name, kws in negatives.items():
    if camp_name in campaign_ids:
        camp_id = campaign_ids[camp_name]
        for kw in kws:
            op = client.get_type("CampaignCriterionOperation")
            op.create.campaign = client.get_service("CampaignService").campaign_path(customer_id, camp_id)
            op.create.negative = True
            op.create.keyword.text = kw
            op.create.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
            neg_ops.append(op)
            print(f"Prepared NEGATIVE EXACT keyword '{kw}' for {camp_name}")

if neg_ops:
    campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=neg_ops)
    print(f"Successfully added {len(neg_ops)} negative keywords!")

print("\n=== All operations completed successfully! ===")
