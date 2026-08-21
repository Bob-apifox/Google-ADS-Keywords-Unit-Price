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

target_ad_groups = [
    'Postman-Alternative-DE-2026', 'Apidog-DE', 'Postman-ID', 
    'Smart-Mock-Server', 'ReadyAPI', 'Katalon-Karate', 'Stoplight Alternative--Global'
]

# Get the Ad Group IDs
query = f"""
    SELECT ad_group.id, ad_group.name, campaign.name
    FROM ad_group
    WHERE ad_group.name IN ('{"', '".join(target_ad_groups)}')
    AND ad_group.status != 'REMOVED'
"""
response = ga_service.search(customer_id=customer_id, query=query)
ad_group_ids = [str(row.ad_group.id) for row in response]
print("Found Ad Groups:", ad_group_ids)

if not ad_group_ids:
    print("No ad groups found.")
    sys.exit()

# Get existing non-broad keywords for these ad groups
kw_query = f"""
    SELECT ad_group_criterion.ad_group, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
    FROM ad_group_criterion
    WHERE ad_group_criterion.type = 'KEYWORD'
    AND ad_group_criterion.status = 'ENABLED'
    AND ad_group.id IN ({", ".join(ad_group_ids)})
"""
kw_response = ga_service.search(customer_id=customer_id, query=kw_query)

operations = []
seen = set()

for row in kw_response:
    ag_res_name = row.ad_group_criterion.ad_group
    kw_text = row.ad_group_criterion.keyword.text
    match_type = row.ad_group_criterion.keyword.match_type
    
    # We want to add Broad match if it's not broad
    if match_type.name != 'BROAD':
        key = f"{ag_res_name}::{kw_text}"
        if key not in seen:
            seen.add(key)
            
            operation = client.get_type('AdGroupCriterionOperation')
            criterion = operation.create
            criterion.ad_group = ag_res_name
            criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            criterion.keyword.text = kw_text
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
            operations.append(operation)
            print(f"Duplicating to BROAD: {kw_text} for {ag_res_name}")

if operations:
    res = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=operations
    )
    print(f"Successfully added {len(operations)} Broad Match keywords.")
else:
    print("No new keywords needed.")
