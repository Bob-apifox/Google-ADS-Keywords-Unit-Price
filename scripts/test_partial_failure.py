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

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    
    # 1. Let's get ONE ad group we created to test keyword upload
    query = "SELECT ad_group.id, ad_group.name, campaign.name FROM ad_group WHERE ad_group.name = 'Postman-Alternative-AR-2026'"
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    ag_id = None
    for batch in stream:
        for row in batch.results:
            ag_id = row.ad_group.id
            break
            
    if not ag_id:
        print("Ad group not found.")
        return
        
    ag_path = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
    
    # 2. Try to add one keyword
    agc_service = client.get_service('AdGroupCriterionService')
    agc = client.get_type('AdGroupCriterionOperation')
    agc.create.ad_group = ag_path
    agc.create.keyword.text = "test postman alternative"
    agc.create.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
    agc.create.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    
    kw_req = client.get_type('MutateAdGroupCriteriaRequest')
    kw_req.customer_id = CUSTOMER_ID
    kw_req.operations.append(agc)
    kw_req.partial_failure = True
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            print("Uploading test keyword...")
            response = agc_service.mutate_ad_group_criteria(request=kw_req)
            
            if response.partial_failure_error and response.partial_failure_error.details:
                for error in response.partial_failure_error.details:
                    print(f"Partial Failure Error: {error}")
            else:
                print("Success without partial failure!")
                for result in response.results:
                    print(f"Result: {result.resource_name}")
            break
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)

if __name__ == '__main__':
    main()
