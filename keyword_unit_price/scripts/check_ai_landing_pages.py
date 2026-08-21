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

def get_landing_pages():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    except:
        time.sleep(2)
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        
    ga_service = client.get_service("GoogleAdsService")
    campaign_name = "Google-Sa-Solutions-AI-LLM-Global"
    
    query = f"""
        SELECT 
            ad_group.name, 
            ad_group_ad.ad.final_urls 
        FROM ad_group_ad 
        WHERE campaign.name = '{campaign_name}' 
        AND ad_group_ad.status = 'ENABLED'
        AND ad_group.status = 'ENABLED'
    """
    
    print(f"--- Landing Pages (Final URLs) in {campaign_name} ---")
    
    seen = set()
    
    for _ in range(5):
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    ag_name = row.ad_group.name
                    urls = row.ad_group_ad.ad.final_urls
                    if urls:
                        url = urls[0]
                        if f"{ag_name}::{url}" not in seen:
                            print(f"[{ag_name}] -> {url}")
                            seen.add(f"{ag_name}::{url}")
            return
        except Exception as e:
            time.sleep(2)
            
if __name__ == "__main__":
    get_landing_pages()
