import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga = client.get_service('GoogleAdsService')

groups = [
    'Compare-Best-Stoplight-Alt-2026',
    'Compare-Best-Mintlify-Alt-2026',
    'Compare-Best-Readme-Alt-2026',
    'Compare-Best-Insomnia-Alt-2026',
    'Compare-Best-Bruno-Alt-2026',
    'Compare-Best-Hoppscotch-Alt-2026',
    'Compare-Best-RapidAPI-Alt-2026'
]

q = "SELECT ad_group.name, ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group.name IN (" + ", ".join([f"'{g}'" for g in groups]) + ") AND ad_group_ad.status = 'ENABLED'"
counts = {g: 0 for g in groups}
for batch in ga.search_stream(customer_id='9496728294', query=q):
    for row in batch.results:
        counts[row.ad_group.name] += 1
        
for g, c in counts.items():
    print(f"AdGroup '{g}' has {c} enabled ads.")
