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

# Find the Postman Alternative ad group
q = """
    SELECT campaign.name, ad_group.id, ad_group.name, ad_group.resource_name 
    FROM ad_group 
    WHERE campaign.name LIKE '%Google-Sa-CP-Global%' 
      AND ad_group.name LIKE '%Postman Alternative%'
      AND ad_group.status = 'ENABLED'
"""
stream = ga_service.search_stream(customer_id=customer_id, query=q)

ag_res_name = None
camp_name = ""
for batch in stream:
    for row in batch.results:
        print(f"Found AdGroup: {row.ad_group.name} in Campaign: {row.campaign.name}")
        ag_res_name = row.ad_group.resource_name
        camp_name = row.campaign.name
        break
    if ag_res_name:
        break

if not ag_res_name:
    print("Could not find Postman Alternative ad group in Google-Sa-CP-Global.")
    # fallback to any CP campaign containing Postman Alternative ad group
    q = """
        SELECT campaign.name, ad_group.id, ad_group.name, ad_group.resource_name 
        FROM ad_group 
        WHERE ad_group.name LIKE '%Postman Alternative%'
          AND ad_group.status = 'ENABLED'
          AND campaign.status = 'ENABLED'
        LIMIT 1
    """
    stream = ga_service.search_stream(customer_id=customer_id, query=q)
    for batch in stream:
        for row in batch.results:
            print(f"Fallback Found AdGroup: {row.ad_group.name} in Campaign: {row.campaign.name}")
            ag_res_name = row.ad_group.resource_name
            camp_name = row.campaign.name
            break

if not ag_res_name:
    print("Fatal: No Postman Alternative ad group found anywhere.")
    sys.exit(1)

keywords = [
    'postman runner limits alternative',
    'postman fully offline',
    'import postman collections locally'
]

operations = []
for kw in keywords:
    print(f"[{camp_name}] Adding keyword (EXACT): [{kw}]")
    operation = client.get_type('AdGroupCriterionOperation')
    criterion = operation.create
    criterion.ad_group = ag_res_name
    criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    criterion.keyword.text = kw
    criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
    operations.append(operation)

if operations:
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=operations
    )
    print(f"Successfully added {len(response.results)} keywords.")
else:
    print("No keywords added.")
