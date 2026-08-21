import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

explicit_cpa_adjustments = {
    # VSCode (Inherited -> 1.00)
    196667184134: 1.00,
    198718724380: 1.00,
    200849963191: 1.00,
    
    # Design (1.15 -> 0.92)
    180298845744: 0.92,
    192948051338: 0.92,
    
    # SpecFirst (2.50 -> 2.00)
    196611085439: 2.00,
    196611085599: 2.00,
    
    # API Editor (2.50 -> 2.00)
    190760245896: 2.00,
    190760246056: 2.00,
    196044288665: 2.00,
    
    # CP-Global (0.67 -> 0.80)
    174276878794: 0.80,
    
    # Scalar-Global (1.46 -> 1.75)
    189613763486: 1.75,
    
    # Horizon (Inherited -> 2.50)
    195076120319: 2.50,
    195934191756: 2.50,
    197378343282: 2.50,
    197378364922: 2.50,
    199560369247: 2.50,
    199560690847: 2.50,
    
    # Bump.sh-Global (2.18 -> 2.50)
    198049379948: 2.50
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('AdGroupService')
    
    operations = []
    
    for ag_id, target in explicit_cpa_adjustments.items():
        target_micros = int(target * 1000000)
        
        ag_op = client.get_type('AdGroupOperation')
        ag_op.update.resource_name = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
        ag_op.update.target_cpa_micros = target_micros
        
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
            print(f'Successfully updated {len(operations)} ad groups with EXPLICIT Target CPAs.')
        except Exception as e:
            print(f'Error updating ad groups: {e}')
    else:
        print('No ad groups to update.')

if __name__ == '__main__':
    main()
