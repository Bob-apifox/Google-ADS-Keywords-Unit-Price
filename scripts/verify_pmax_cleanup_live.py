import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    # 1. Check PMax Postman status
    q_pmax = "SELECT campaign.id, campaign.name, campaign.status FROM campaign WHERE campaign.id = 23685533966"
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_pmax):
        for row in batch.results:
            print(f"[CAMPAIGN STATUS] {row.campaign.name} (ID: {row.campaign.id}) -> Status: {row.campaign.status.name}")

    # 2. Check Customer Negative Placements count
    q_neg = "SELECT customer_negative_criterion.id, customer_negative_criterion.placement.url FROM customer_negative_criterion WHERE customer_negative_criterion.type = 'PLACEMENT'"
    count = 0
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_neg):
        for row in batch.results:
            count += 1
    print(f"[ACCOUNT EXCLUSIONS] Total active account-level placement exclusions: {count}")

if __name__ == '__main__':
    main()
