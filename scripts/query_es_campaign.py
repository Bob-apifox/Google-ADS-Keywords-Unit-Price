# -*- coding: utf-8 -*-
import os
import sys
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
    query = """
        SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.experiment_type
        FROM campaign
        WHERE campaign.name LIKE '%Google-Sa-CP-ES%'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    for batch in stream:
        for row in batch.results:
            print(f"ID: {row.campaign.id} | Name: {row.campaign.name} | Status: {row.campaign.status} | Type: {row.campaign.advertising_channel_type} | ExpType: {row.campaign.experiment_type}")

if __name__ == '__main__':
    main()
