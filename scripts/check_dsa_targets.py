import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')

q = """
    SELECT 
        ad_group.name, 
        ad_group_criterion.webpage.conditions 
    FROM ad_group_criterion 
    WHERE campaign.name = 'Google-Sa-DSA-Global' 
      AND ad_group_criterion.type = 'WEBPAGE'
"""
for batch in ga_service.search_stream(customer_id='9496728294', query=q):
    for row in batch.results:
        conditions = row.ad_group_criterion.webpage.conditions
        cond_strs = []
        for c in conditions:
            cond_strs.append(f"{c.argument}")
        print(f"AdGroup: {row.ad_group.name} -> Target URLs containing: {', '.join(cond_strs)}")
