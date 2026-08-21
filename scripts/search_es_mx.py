# -*- coding: utf-8 -*-
import os, sys, urllib3
from google.ads.googleads.client import GoogleAdsClient

try: sys.stdout.reconfigure(encoding='utf-8')
except: pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    query = "SELECT campaign.id, campaign.name, campaign.status FROM campaign"
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    
    print("\n=== ALL CAMPAIGNS IN ACCOUNT ===")
    for batch in stream:
        for row in batch.results:
            name = row.campaign.name
            cid = row.campaign.id
            status = row.campaign.status.name
            if any(k in name.upper() for k in ["ES", "MX", "SPANISH", "MEXICO", "LATAM"]):
                print(f" -> Found: {name} (ID: {cid}), Status: {status}")

if __name__ == '__main__':
    main()
