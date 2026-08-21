import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

client = GoogleAdsClient.load_from_storage(r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml")
customer_id = "9496728294"

ag_criterion_service = client.get_service("AdGroupCriterionService")

keywords_to_update = [
    {"campaign": "Google-Sa-Testing-Global", "text": "api security testing tool"},
    {"campaign": "Google-Sa-Func-MultiProtocol-Global", "text": "test sse stream endpoint"}
]

for kw in keywords_to_update:
    query = f"""
        SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type 
        FROM ad_group_criterion 
        WHERE campaign.name = '{kw['campaign']}' 
          AND ad_group_criterion.type = 'KEYWORD'
          AND ad_group_criterion.keyword.text = '{kw['text']}'
          AND ad_group_criterion.status = 'ENABLED'
    """
    response = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=query)
    found = False
    for row in response:
        found = True
        print(f"Found criterion: {row.ad_group_criterion.resource_name} with match type {row.ad_group_criterion.keyword.match_type.name}")
        if row.ad_group_criterion.keyword.match_type != client.enums.KeywordMatchTypeEnum.EXACT:
            # Note: We cannot change match_type of an existing keyword. We must pause/remove it and create a new one.
            # 1. Pause old
            op_pause = client.get_type("AdGroupCriterionOperation")
            op_pause.update.resource_name = row.ad_group_criterion.resource_name
            op_pause.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
            from google.api_core import protobuf_helpers
            client.copy_from(op_pause.update_mask, protobuf_helpers.field_mask(None, op_pause.update._pb))
            ag_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=[op_pause])
            print(f"Paused old broad keyword {kw['text']}")

            # 2. Extract ad group from resource name
            ad_group_id = row.ad_group_criterion.resource_name.split("/")[-1].split("~")[0]
            ad_group_res = f"customers/{customer_id}/adGroups/{ad_group_id}"

            # 3. Create new Exact
            op_create = client.get_type("AdGroupCriterionOperation")
            criterion = op_create.create
            criterion.ad_group = ad_group_res
            criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            criterion.keyword.text = kw['text']
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
            
            ag_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=[op_create])
            print(f"Created new exact match keyword [{kw['text']}]")
    if not found:
        print(f"Keyword '{kw['text']}' not found in {kw['campaign']}")
