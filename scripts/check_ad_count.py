import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
query = """SELECT campaign.name, ad_group.name, ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND campaign.name LIKE '%Google-Sa-CP-%'"""
stream = ga_service.search_stream(customer_id='9496728294', query=query)
camps = {}
for batch in stream:
    for row in batch.results:
        camps[row.campaign.name] = camps.get(row.campaign.name, 0) + 1
print(camps)
