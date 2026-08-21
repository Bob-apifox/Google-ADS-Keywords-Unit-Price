import os
from google.ads.googleads.client import GoogleAdsClient

# Setup proxy
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

IDS = [2016, 2156, 2316, 2344, 2580, 2581, 2630, 2643, 2840, 2850, 2076, 2360]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    
    query = f"""
        SELECT 
            geo_target_constant.id, 
            geo_target_constant.name, 
            geo_target_constant.canonical_name, 
            geo_target_constant.country_code 
        FROM geo_target_constant 
        WHERE geo_target_constant.id IN ({','.join([str(i) for i in IDS])})
    """
    
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    for batch in stream:
        for row in batch.results:
            print(f"ID: {row.geo_target_constant.id} | Name: {row.geo_target_constant.name} | Canonical: {row.geo_target_constant.canonical_name} | Country Code: {row.geo_target_constant.country_code}")

if __name__ == "__main__":
    main()
