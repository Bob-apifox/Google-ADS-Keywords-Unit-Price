import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

def get_existing_groups():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    except:
        time.sleep(2)
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        
    ga_service = client.get_service("GoogleAdsService")
    campaign_name = "Google-Sa-Solutions-AI-LLM-Global"
    
    query = f"""
        SELECT 
            ad_group.id, 
            ad_group.name, 
            ad_group.target_cpa_micros 
        FROM ad_group 
        WHERE campaign.name = '{campaign_name}' 
        AND ad_group.status = 'ENABLED'
    """
    
    print(f"--- Existing Ad Groups in {campaign_name} ---")
    
    for _ in range(5):
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    cpa = getattr(row.ad_group, 'target_cpa_micros', 0)
                    cpa_usd = cpa / 1e6 if cpa else 0
                    print(f"Ad Group: {row.ad_group.name} | CPA: ${cpa_usd:.2f}")
            return
        except Exception as e:
            time.sleep(2)
            
if __name__ == "__main__":
    get_existing_groups()
