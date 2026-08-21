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

    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('AdGroupService')
    
    operations = []
    updated_info = []
    
    for row in ag_data:
        ag_id = row['ad_group_id']
        cpa = row['actual_cpa']
        conv = row['conversions']
        
        if conv > 0:
            target = min(cpa * 1.2, 2.5)
            target = max(target, 0.5)
        else:
            target = 2.5
            
        target_micros = int(target * 1000000)
        
        ag_op = client.get_type('AdGroupOperation')
        ag_op.update.resource_name = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
        ag_op.update.target_cpa_micros = target_micros
        
        client.copy_from(
            ag_op.update_mask,
            protobuf_helpers.field_mask(None, type(ag_op.update).pb(ag_op.update))
        )
        operations.append(ag_op)
        updated_info.append(f"{row['ad_group_name']}: ${target:.2f}")
        
    if operations:
        try:
            request = client.get_type('MutateAdGroupsRequest')
            request.customer_id = CUSTOMER_ID
            request.operations.extend(operations)
            request.partial_failure = True
            
            response = ga_service.mutate_ad_groups(request=request)
            print(f'Successfully updated {len(operations)} ad groups with dynamic CPA.')
            print('Sample updates:', ', '.join(updated_info[:5]))
        except Exception as e:
            print(f'Error updating ad groups: {e}')
    else:
        print('No ad groups to update.')

if __name__ == '__main__':
    main()
