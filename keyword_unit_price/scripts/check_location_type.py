import os
from google.ads.googleads.client import GoogleAdsClient

# Setup proxy
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

TARGET_CAMPAIGNS = ["Google-Sa-CP-Global", "Google-Sa-Postman-Global"]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    
    query = """
        SELECT 
            campaign.id,
            campaign.name,
            campaign_criterion.criterion_id,
            campaign_criterion.location.geo_target_constant,
            campaign_criterion.negative
        FROM campaign_criterion
        WHERE campaign_criterion.type = 'LOCATION'
    """
    
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            if c_name in TARGET_CAMPAIGNS:
                print(f"Campaign: {c_name} | Location: {row.campaign_criterion.location.geo_target_constant} | Negative/Excluded: {row.campaign_criterion.negative} | ID: {row.campaign_criterion.criterion_id}")

if __name__ == "__main__":
    main()
