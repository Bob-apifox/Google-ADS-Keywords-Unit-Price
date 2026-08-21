import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

keywords_to_expand = [
    "postman alternative",
    "api testing tools",
    "api tools like postman",
    "postman alternatives",
    "api doc generator",
    "apidoc",
    "postman open source alternative",
    "api testing",
    "postman online",
    "hoppscotch"
]

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")
ad_group_criterion_service = client.get_service("AdGroupCriterionService")
ad_group_service = client.get_service("AdGroupService")

# Fetch existing keywords to find their ad groups. Exclude DSA.
kw_list_str = ", ".join([f"'{k}'" for k in keywords_to_expand])
query = f"""
    SELECT
        ad_group.id,
        ad_group.name,
        ad_group.type,
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type
    FROM ad_group_criterion
    WHERE ad_group_criterion.type = 'KEYWORD'
      AND ad_group_criterion.status = 'ENABLED'
      AND ad_group.status = 'ENABLED'
      AND campaign.status = 'ENABLED'
      AND ad_group.type = 'SEARCH_STANDARD'
      AND ad_group_criterion.keyword.text IN ({kw_list_str})
"""

stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)

existing_adgroup_kws = {}
for batch in stream:
    for row in batch.results:
        ag_id = row.ad_group.id
        kw_text = row.ad_group_criterion.keyword.text
        match_type = row.ad_group_criterion.keyword.match_type.name
        
        key = (ag_id, kw_text)
        if key not in existing_adgroup_kws:
            existing_adgroup_kws[key] = set()
        existing_adgroup_kws[key].add(match_type)

operations = []
added_combinations = set()

for (ag_id, kw_text), match_types in existing_adgroup_kws.items():
    if "BROAD" not in match_types:
        if (ag_id, kw_text) not in added_combinations:
            op = client.get_type("AdGroupCriterionOperation")
            criterion = op.create
            criterion.ad_group = ad_group_service.ad_group_path(CUSTOMER_ID, ag_id)
            criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            criterion.keyword.text = kw_text
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
            operations.append(op)
            added_combinations.add((ag_id, kw_text))
            print(f"Prepared BROAD match for '{kw_text}' in Ad Group ID: {ag_id}")

if operations:
    print(f"Total new BROAD match keywords to add: {len(operations)}")
    try:
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=CUSTOMER_ID, operations=operations
        )
        for result in response.results:
            print(f"Added Criterion: {result.resource_name}")
    except Exception as e:
        print(f"Failed to add criteria: {e}")
else:
    print("No new BROAD match keywords needed. They might already exist or the exact matches weren't found in active standard ad groups.")
