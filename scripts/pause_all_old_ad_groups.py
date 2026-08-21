# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib3
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

campaign_ids = [
    21995819717, 21995977112, 23139757330, 22261650381, 21965514943,
    22309414047, 23264160392, 22374204671, 22451766179, 22367960103,
    23027715066, 23047433007
]

def parse_mask(paths):
    from google.protobuf.field_mask_pb2 import FieldMask
    return FieldMask(paths=paths)

def execute():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    ad_group_service = client.get_service('AdGroupService')
    
    ids_str = ", ".join(map(str, campaign_ids))
    query = f"""
        SELECT ad_group.id, ad_group.name, ad_group.status, campaign.id, campaign.name
        FROM ad_group
        WHERE campaign.id IN ({ids_str})
          AND ad_group.status = 'ENABLED'
    """
    
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    pause_ops = []
    
    for batch in stream:
        for row in batch.results:
            ag_name = row.ad_group.name
            ag_id = row.ad_group.id
            if not ag_name.startswith("Postman-Alternative-"):
                print(f"Pausing Old Enabled Ad Group: '{ag_name}' (ID: {ag_id}) in Campaign '{row.campaign.name}'")
                ag_op = client.get_type('AdGroupOperation')
                ag = ag_op.update
                ag.resource_name = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
                ag.status = client.enums.AdGroupStatusEnum.PAUSED
                client.copy_from(ag_op.update_mask, parse_mask(["status"]))
                pause_ops.append(ag_op)
            else:
                print(f"Keeping New 2026 Ad Group ENABLED: '{ag_name}' (ID: {ag_id}) in Campaign '{row.campaign.name}'")

    if pause_ops:
        response = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=pause_ops)
        print(f"\n[SUCCESS] Successfully paused {len(response.results)} old Ad Groups!")
    else:
        print("\n[INFO] Clean! No old enabled Ad Groups found.")
    return True

def main():
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}/{max_retries}...")
            if execute():
                break
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(2)

if __name__ == '__main__':
    main()
