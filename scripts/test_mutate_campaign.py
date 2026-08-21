# -*- coding: utf-8 -*-
import os
import sys
import urllib3
import time
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

def parse_mask(paths):
    from google.protobuf.field_mask_pb2 import FieldMask
    return FieldMask(paths=paths)

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    campaign_service = client.get_service('CampaignService')
    ga_service = client.get_service('GoogleAdsService')
    
    camp_op = client.get_type('CampaignOperation')
    campaign = camp_op.update
    campaign.resource_name = ga_service.campaign_path(CUSTOMER_ID, 23696756393)
    campaign.status = client.enums.CampaignStatusEnum.ENABLED
    client.copy_from(camp_op.update_mask, parse_mask(["status"]))
    
    request = client.get_type('MutateCampaignsRequest')
    request.customer_id = CUSTOMER_ID
    request.operations = [camp_op]
    request.partial_failure = True
    
    try:
        response = campaign_service.mutate_campaigns(request=request)
        for result in response.results:
            print(f"Success! Mutated: {result.resource_name}")
        for error in response.partial_failure_error.details:
            print(f"Error: {error}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == '__main__':
    main()
