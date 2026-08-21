# -*- coding: utf-8 -*-
import os
import sys
import json
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

def get_geo_ids():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    
    countries = ["ES", "MX", "BR", "PT", "JP", "KR", "TW", "VN", "ID", "DE", "FR", "TR"]
    country_quotes = ",".join([f"'{c}'" for c in countries])
    
    query = f"""
        SELECT geo_target_constant.id, geo_target_constant.canonical_name, geo_target_constant.country_code
        FROM geo_target_constant
        WHERE geo_target_constant.canonical_name LIKE '%Taiwan%'
    """
    
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    
    for batch in stream:
        for row in batch.results:
            print(f"{row.geo_target_constant.country_code}: {row.geo_target_constant.id} - {row.geo_target_constant.canonical_name}")

if __name__ == '__main__':
    get_geo_ids()
