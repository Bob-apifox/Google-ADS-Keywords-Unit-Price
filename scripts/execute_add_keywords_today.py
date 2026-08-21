import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
ad_group_criterion_service = client.get_service('AdGroupCriterionService')
customer_id = '9496728294'

# We need to find the ad groups for these campaigns to add the keywords to.
# We will just pick the first active ad group in each campaign.
additions = {
    'Google-Sa-CP-AR': ['بديل postman', 'اختبار api مجاني'],
    'Google-Sa-The "Great Migration"-26': ['migrate swagger to apidog', 'import insomnia to postman alternative']
}

# Find active ad groups
q = "SELECT campaign.name, ad_group.id, ad_group.resource_name FROM ad_group WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED'"
stream = ga_service.search_stream(customer_id=customer_id, query=q)

camp_to_adgroup = {}
for batch in stream:
    for row in batch.results:
        camp_name = row.campaign.name
        if camp_name in additions and camp_name not in camp_to_adgroup:
            camp_to_adgroup[camp_name] = row.ad_group.resource_name

operations = []
for camp_name, kws in additions.items():
    if camp_name not in camp_to_adgroup:
        print(f"Warning: Could not find active Ad Group for campaign: {camp_name}")
        continue
    
    ag_res_name = camp_to_adgroup[camp_name]
    
    for kw in kws:
        print(f"[{camp_name}] Adding keyword: [{kw}]")
        operation = client.get_type('AdGroupCriterionOperation')
        criterion = operation.create
        criterion.ad_group = ag_res_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = kw
        if "Great Migration" in camp_name:
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        else:
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
        operations.append(operation)

if operations:
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=operations
    )
    print(f"Successfully added {len(response.results)} keywords.")
else:
    print("No keywords added.")
