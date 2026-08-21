import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')

urls_to_check = [
    'top-postman-alternative-open-source',
    'postman-to-openapi',
    'top-6-soap-api-documentation-tools',
    'best-swagger-alternatives',
    '/compare/apidog-vs-postman/',
    '/api-doc/',
    '/api-mocking/'
]

q = "SELECT ad_group.name, ad_group_criterion.webpage.conditions FROM ad_group_criterion WHERE campaign.name = 'Google-Sa-DSA-Global' AND ad_group_criterion.type = 'WEBPAGE' AND ad_group_criterion.status = 'ENABLED'"
existing_targets = []
for batch in ga_service.search_stream(customer_id='9496728294', query=q):
    for row in batch.results:
        for cond in row.ad_group_criterion.webpage.conditions:
            existing_targets.append((row.ad_group.name, cond.argument))
            
print("--- Currently Existing DSA Targets Matching Your List ---")
for url in urls_to_check:
    found = False
    for ag, target in existing_targets:
        if url in target or target in url:
            print(f"[EXISTS] '{url}' is covered by AdGroup '{ag}' (Rule: {target})")
            found = True
    if not found:
        print(f"[MISSING] '{url}' is NOT found in any active DSA AdGroup.")
