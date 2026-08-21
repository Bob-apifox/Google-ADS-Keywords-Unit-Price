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

target_campaigns = [
    "Google-Sa-CP-ES", "Google-Sa-CP-MX", "Google-Sa-CP-AR", "Google-Sa-CP-PT",
    "Google-Sa-CP-JP", "Google-Sa-CP-KR", "Google-Sa-CP-TW", "Google-Sa-CP-VN",
    "Google-Sa-CP-ID", "Google-Sa-CP-DE", "Google-Sa-CP-FR", "Google-Sa-CP-TR"
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    
    query = """
        SELECT campaign.id, campaign.name, ad_group.id, ad_group.name, ad_group.status
        FROM ad_group
        WHERE campaign.name LIKE '%Google-Sa-CP-%'
    """
    
    max_retries = 10
    for attempt in range(max_retries):
        try:
            print(f"Fetching Ad Groups, Attempt {attempt+1}...")
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            
            campaign_map = {}
            for batch in stream:
                for row in batch.results:
                    c_name = row.campaign.name
                    if c_name not in campaign_map:
                        campaign_map[c_name] = []
                    campaign_map[c_name].append({
                        "ag_name": row.ad_group.name,
                        "ag_status": row.ad_group.status.name,
                        "ag_id": row.ad_group.id
                    })
                    
            # Print in an organized way
            for c_name, groups in campaign_map.items():
                # Only care about our targets (and any misnamed ones)
                if any(tc.lower() in c_name.lower() for tc in target_campaigns):
                    print(f"\n[{c_name}]")
                    for g in groups:
                        print(f"  -> Ad Group: {g['ag_name']} | Status: {g['ag_status']} | ID: {g['ag_id']}")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

if __name__ == '__main__':
    main()
