import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service('GoogleAdsService')

campaign_names = [
    'Google-Sa-Comp-VSCode-Global',
    'Google-Sa-Comp-HeavyQA-Global',
    'Google-Sa-Comp-StaticDocs-Global',
    'Google-Sa-Func-ContractTest-Global',
    'Google-Sa-Func-CICD-Global',
    'Google-Sa-Func-MultiProtocol-Global',
    'Google-Sa-Func-AdvancedMock-Global'
]

print("Fetching Campaign IDs...")
query = f'''
    SELECT campaign.id, campaign.name
    FROM campaign
    WHERE campaign.name IN ({", ".join([f"'{name}'" for name in campaign_names])})
'''

stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
found = 0
for batch in stream:
    for row in batch.results:
        print(f"'{row.campaign.name}': '{row.campaign.id}'")
        found += 1

print(f"Found {found}/{len(campaign_names)} campaigns.")
