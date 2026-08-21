import os
from google.ads.googleads.client import GoogleAdsClient
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'
client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
query = """SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.status FROM ad_group_ad WHERE campaign.name LIKE '%ESP-2%'"""
stream = ga_service.search_stream(customer_id='9496728294', query=query)
for batch in stream:
    for row in batch.results:
        print(f'{row.campaign.name} | {row.ad_group.name} | {row.ad_group_ad.status.name}')
