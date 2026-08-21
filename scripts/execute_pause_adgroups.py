import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
ad_group_service = client.get_service('AdGroupService')
customer_id = '9496728294'

targets = {
    'Google-Sa-CLI-Global': ['Terminal-Native-Clients'],
    'Google-Sa-Func-AdvancedMock-Global': ['Service-Virtualization'],
    'Google-Sa-Stoplight-Global': ['Stoplight-Features--Global']
}

q = "SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.name IN ('Google-Sa-CLI-Global', 'Google-Sa-Func-AdvancedMock-Global', 'Google-Sa-Stoplight-Global') AND ad_group.status != 'REMOVED'"

stream = ga_service.search_stream(customer_id=customer_id, query=q)

operations = []
for batch in stream:
    for row in batch.results:
        camp_name = row.campaign.name
        ag_name = row.ad_group.name
        if camp_name in targets and ag_name in targets[camp_name]:
            print(f"Pausing AdGroup '{ag_name}' in Campaign '{camp_name}' (ID: {row.ad_group.id})")
            
            operation = client.get_type('AdGroupOperation')
            ad_group = operation.update
            ad_group.resource_name = row.ad_group.resource_name
            ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
            fm = protobuf_helpers.field_mask(None, type(operation.update).pb(operation.update))
            client.copy_from(operation.update_mask, fm)
            operations.append(operation)

if operations:
    response = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=operations)
    print(f"Successfully paused {len(response.results)} ad groups.")
else:
    print("No matching active ad groups found to pause.")
