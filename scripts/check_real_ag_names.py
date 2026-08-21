import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')

q = "SELECT campaign.name, ad_group.name FROM ad_group WHERE campaign.name IN ('Google-Sa-Comp-VSCode-Global', 'Google-Sa-Insomnia-Global', 'Google-Sa-Brand-Global')"
for batch in ga_service.search_stream(customer_id='9496728294', query=q):
    for row in batch.results:
        print(f"{row.campaign.name} -> {row.ad_group.name}")
