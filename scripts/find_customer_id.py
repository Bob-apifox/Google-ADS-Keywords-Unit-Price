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

def main():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt+1}...")
            client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
            ga_service = client.get_service('GoogleAdsService')
            query = """
                SELECT campaign.id, campaign.name, customer.id
                FROM campaign
            """
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    name = row.campaign.name
                    name_lower = name.lower()
                    if "google-sa-cp-es" in name_lower or "google-sa-solutions-ai-llm-global" in name_lower:
                        print(f"Campaign: {name} | Camp ID: {row.campaign.id} | Customer ID: {row.customer.id}")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

if __name__ == '__main__':
    main()
