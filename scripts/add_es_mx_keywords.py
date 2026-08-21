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

es_mx_keywords = {
    178550275834: ["alternativas a postman", "alternativa a postman gratis", "postman gratis", "postman espanol"], # ES
    178550276074: ["alternativas a postman", "postman mexico gratis", "probador de api gratis", "alternativa postman gratis"] # MX
}

def execute():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ad_group_criterion_service = client.get_service('AdGroupCriterionService')
    ga_service = client.get_service('GoogleAdsService')
    
    kw_ops = []
    total = 0
    for ag_id, words in es_mx_keywords.items():
        ag_path = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
        for w in words:
            # Phrase
            op_p = client.get_type('AdGroupCriterionOperation')
            op_p.create.ad_group = ag_path
            op_p.create.keyword.text = w
            op_p.create.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            op_p.create.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw_ops.append(op_p)
            total += 1
            
            # Exact
            op_e = client.get_type('AdGroupCriterionOperation')
            op_e.create.ad_group = ag_path
            op_e.create.keyword.text = w
            op_e.create.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
            op_e.create.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw_ops.append(op_e)
            total += 1

    if kw_ops:
        request = client.get_type('MutateAdGroupCriteriaRequest')
        request.customer_id = CUSTOMER_ID
        request.operations.extend(kw_ops)
        request.partial_failure = True
        response = ad_group_criterion_service.mutate_ad_group_criteria(request=request)
        print(f"✅ SUCCESS: Added {total} Phrase & Exact keywords to ES & MX Ad Groups!")
    return True

def main():
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            if execute():
                break
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(2)

if __name__ == '__main__':
    main()
