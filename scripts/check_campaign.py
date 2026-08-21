import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

client = GoogleAdsClient.load_from_storage(r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml")
customer_id = "9496728294"

query = "SELECT campaign.id, campaign.name, campaign.resource_name FROM campaign WHERE campaign.name LIKE '%DSA-Alternatives%'"
response = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=query)
for row in response:
    print(row.campaign.name, row.campaign.resource_name)
