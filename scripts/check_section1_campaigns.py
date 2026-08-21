# -*- coding: utf-8 -*-
import os
import sys
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

target_campaigns = [
    "Google-Sa-CP-ES", "Google-Sa-CP-MX", "Google-Sa-CP-AR", "Google-Sa-CP-PT",
    "Google-Sa-CP-JP", "Google-Sa-CP-KR", "Google-Sa-CP-TW", "Google-Sa-CP-VN",
    "Google-Sa-CP-ID", "Google-Sa-CP-DE", "Google-Sa-CP-FR", "Google-Sa-CP-TR"
]

def main():
    print(">>> Connecting to Google Ads API...")
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    
    query = """
        SELECT campaign.id, campaign.name, campaign.status, campaign.tracking_url_template, campaign.final_url_suffix
        FROM campaign
    """
    
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    found_camps = {}
    
    print("\n=== ACCOUNT CAMPAIGNS SEARCH ===")
    for batch in stream:
        for row in batch.results:
            name = row.campaign.name
            for tc in target_campaigns:
                if tc.lower() in name.lower():
                    found_camps[tc] = {
                        "id": row.campaign.id,
                        "real_name": name,
                        "status": row.campaign.status.name,
                        "tracking_template": row.campaign.tracking_url_template,
                        "final_url_suffix": row.campaign.final_url_suffix
                    }
                    
    for tc in target_campaigns:
        if tc in found_camps:
            info = found_camps[tc]
            print(f"✅ Found: [{tc}] -> Real Name: '{info['real_name']}' (ID: {info['id']}), Status: {info['status']}, Suffix: '{info['final_url_suffix']}'")
        else:
            print(f"❌ Missing: [{tc}] (Not found in account)")

if __name__ == '__main__':
    main()
