import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')

camps = [
    'Google-Sa-Postman-Global',
    'Google-Sa-Bruno-Global',
    'Google-Sa-Hoppscotch-Global',
    'Google-Sa-RapidAPI-Global',
    'Google-Sa-Comp-VSCode-Global',
    'Google-Sa-Insomnia-Global',
    'Google-Sa-Swagger-Global',
    'Google-Sa-Brand-Global',
    'Google-Sa-Solutions-AI-LLM-Global'
]

q = "SELECT campaign.name, campaign.keyword_match_type FROM campaign WHERE campaign.name IN (" + ", ".join([f"'{c}'" for c in camps]) + ")"
stream = ga_service.search_stream(customer_id='9496728294', query=q)

for batch in stream:
    for row in batch.results:
        print(f"{row.campaign.name}: {row.campaign.keyword_match_type.name}")
