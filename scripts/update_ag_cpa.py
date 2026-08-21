# -*- coding: utf-8 -*-
import os
import json
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

def main():
    with open('ag_analysis.json', 'r', encoding='utf-8') as f:
        ag_data = json.load(f)
        
    ad_group_ids = list(set([item['ad_group_id'] for item in ag_data]))
    print(f'Found {len(ad_group_ids)} ad groups to update.')

    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('AdGroupService')
    
    operations = []
    for ag_id in ad_group_ids:
        ag_op = client.get_type('AdGroupOperation')
        ag_op.update.resource_name = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
        # Set Target CPA to 2.5 million micros (.50)
        ag_op.update.target_cpa_micros = 2500000
        
        client.copy_from(
            ag_op.update_mask,
            protobuf_helpers.field_mask(None, type(ag_op.update).pb(ag_op.update))
        )
        operations.append(ag_op)
        
    if operations:
        try:
            request = client.get_type('MutateAdGroupsRequest')
            request.customer_id = CUSTOMER_ID
            request.operations.extend(operations)
            request.partial_failure = True
            
            response = ga_service.mutate_ad_groups(request=request)
            print(f'✅ Successfully sent update for {len(operations)} ad groups to .5 Target CPA.')
        except Exception as e:
            print(f'Error updating ad groups: {e}')
    else:
        print('No ad groups to update.')

if __name__ == '__main__':
    main()

