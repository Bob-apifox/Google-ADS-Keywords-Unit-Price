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
    "Google-Sa-CP-ID", "Google-Sa-CP-DE", "Google-Sa-CP-FR", "Google-Sa-CP-TR",
    "Google-Sa-CP-ar" # include the arabic one just in case
]

TRACKING_SUFFIX = "utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_term={keyword}"

def apply_tracking_suffix():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    campaign_service = client.get_service('CampaignService')

    query = """
        SELECT campaign.id, campaign.name, campaign.final_url_suffix
        FROM campaign
        WHERE campaign.name LIKE '%Google-Sa-CP-%'
    """
    
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    
    camp_ops = []
    
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            c_id = row.campaign.id
            current_suffix = row.campaign.final_url_suffix
            
            if any(tc.lower() in c_name.lower() for tc in target_campaigns):
                if current_suffix != TRACKING_SUFFIX:
                    print(f"Updating tracking suffix for {c_name} (Current: {current_suffix})")
                    camp_op = client.get_type('CampaignOperation')
                    campaign = camp_op.update
                    campaign.resource_name = ga_service.campaign_path(CUSTOMER_ID, c_id)
                    campaign.final_url_suffix = TRACKING_SUFFIX
                    camp_op.update_mask.paths.append("final_url_suffix")
                    camp_ops.append(camp_op)
                else:
                    print(f"Campaign {c_name} already has the correct tracking suffix.")

    if camp_ops:
        print(f">>> Executing {len(camp_ops)} updates...")
        req = client.get_type('MutateCampaignsRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(camp_ops)
        req.partial_failure = True
        
        resp = campaign_service.mutate_campaigns(request=req)
        
        if resp.partial_failure_error and resp.partial_failure_error.details:
            for error in resp.partial_failure_error.details:
                print(f"Partial Failure: {error}")
        else:
            print(f"[SUCCESS] Updated {len(resp.results)} campaigns with new tracking suffix.")
    else:
        print("No campaigns needed updating.")
        
    return True

def main():
    max_retries = 10
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt+1}/{max_retries}...")
            if apply_tracking_suffix():
                break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == '__main__':
    main()
