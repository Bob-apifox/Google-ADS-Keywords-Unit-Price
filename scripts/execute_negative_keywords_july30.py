import os
import sys
import re
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
campaign_criterion_service = client.get_service('CampaignCriterionService')
customer_id = '9496728294'

campaigns_map = {
    'Google-Sa-CP-DE': '22367960103',
    'Google-Sa-Swagger-Global': '22923613652',
    'Google-Sa-API Editor-Global': '23376992548',
    'Google-Sa-Func-AdvancedMock-Global': '23981409303',
    'Google-Sa-Stoplight-Global': '22892634645',
    'Google-Sa-Mock-Global': '22067541248',
    'Google-Sa-Insomnia-Global': '22806818611',
    'Google-Sa-Fern-Global': '23405430858',
    'Google-Sa-CLI-Global': '23974416637',
    'Google-Sa-Mintlify-Global': '23320166856',
    'Google-Sa-Testing-Global': '22067987413',
    'Google-Sa-Bruno-Global': '23347684482',
    'Google-Sa-Doc-Global': '22061425619',
    'Google-Sa-Scalar-Global': '23405649492',
    'Google-Sa-MCP-Infrastructure': '23864356298',
    'Google-Sa-Hoppscotch-Global': '22976792571'
}

plan_path = r'C:\Users\bobzh\.gemini\antigravity-ide\brain\df619394-c984-4a1b-a06e-a4f08016a39a\implementation_plan.md'
with open(plan_path, 'r', encoding='utf-8') as f:
    plan_text = f.read()

negatives_by_camp = {}
current_camp = None
for line in plan_text.splitlines():
    if line.startswith('#### [MODIFY] Campaign:'):
        current_camp = line.replace('#### [MODIFY] Campaign:', '').strip()
    elif current_camp and '➕ 添加精准否定词' in line:
        match = re.search(r'`\[(.*?)\]`', line)
        if match:
            if current_camp not in negatives_by_camp:
                negatives_by_camp[current_camp] = []
            negatives_by_camp[current_camp].append(match.group(1))

operations = []
for camp_name, kws in negatives_by_camp.items():
    camp_id = campaigns_map.get(camp_name)
    if not camp_id:
        print(f"Unknown campaign ID for {camp_name}")
        continue
    for kw in kws:
        operation = client.get_type('CampaignCriterionOperation')
        criterion = operation.create
        criterion.campaign = client.get_service('CampaignService').campaign_path(customer_id, camp_id)
        criterion.negative = True
        criterion.keyword.text = kw
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
        operations.append(operation)
        print(f"[{camp_name}] Negating: [{kw}]")

if operations:
    response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id, operations=operations
    )
    print(f"Successfully added {len(operations)} negative keywords.")
else:
    print("No negative keywords found to add.")
