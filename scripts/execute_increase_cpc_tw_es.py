# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib3
from google.ads.googleads.client import GoogleAdsClient

try: sys.stdout.reconfigure(encoding='utf-8')
except: pass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

def increase_cpc():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    ad_group_service = client.get_service('AdGroupService')
    
    q_ag = """
        SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.cpc_bid_micros, campaign.name
        FROM ad_group
        WHERE campaign.name IN ('Google-Sa-CP-TW', 'Google-Sa-CP-ESP') 
          AND ad_group.status = 'ENABLED'
    """
    print(">>> Fetching AdGroups in TW and ES campaigns...")
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag)
    
    ag_ops = []
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            ag_name = row.ad_group.name
            ag_id = row.ad_group.id
            current_cpc = row.ad_group.cpc_bid_micros
            
            # Default to 1M if 0 or not set, then increase 20%
            if not current_cpc or current_cpc <= 0:
                new_cpc = int(1000000 * 1.2)  # Base $1.00 -> $1.20
            else:
                new_cpc = int(current_cpc * 1.2)
                
            print(f"[{c_name}] AdGroup: {ag_name} | Old CPC: {current_cpc/1000000 if current_cpc else 0.0} -> New CPC: {new_cpc/1000000}")
            
            op = client.get_type('AdGroupOperation')
            ag = op.update
            ag.resource_name = ad_group_service.ad_group_path(CUSTOMER_ID, ag_id)
            ag.cpc_bid_micros = new_cpc
            op.update_mask.paths.append("cpc_bid_micros")
            ag_ops.append(op)
            
    if ag_ops:
        print(f"Executing {len(ag_ops)} CPC updates...")
        req = client.get_type('MutateAdGroupsRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ag_ops)
        req.partial_failure = True
        resp = ad_group_service.mutate_ad_groups(request=req)
        
        # Handle partial failures if any
        if resp.partial_failure_error and resp.partial_failure_error.message:
            print(f"Partial failures occurred: {resp.partial_failure_error.message}")
        else:
            print("Successfully updated CPC!")
    else:
        print("No enabled AdGroups found to update.")
        
    return True

if __name__ == '__main__':
    try:
        increase_cpc()
    except Exception as e:
        print(f"Error: {e}")
