import os
import sys
import json
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"
CAMPAIGN_ID = "23320166856"

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")

query = f"""
    SELECT
        campaign.id,
        campaign.name,
        ad_group.id,
        ad_group.name,
        ad_group_ad.ad.id,
        ad_group_ad.ad.type,
        ad_group_ad.ad.final_urls,
        ad_group_ad.ad.tracking_url_template,
        ad_group_ad.status,
        ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions
    FROM ad_group_ad
    WHERE campaign.id = {CAMPAIGN_ID}
      AND ad_group_ad.status != 'REMOVED'
"""

stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)

ads_found = []
for batch in stream:
    for row in batch.results:
        headlines = [h.text for h in row.ad_group_ad.ad.responsive_search_ad.headlines]
        descriptions = [d.text for d in row.ad_group_ad.ad.responsive_search_ad.descriptions]
        ad_data = {
            "ad_group_id": row.ad_group.id,
            "ad_group_name": row.ad_group.name,
            "ad_id": row.ad_group_ad.ad.id,
            "ad_type": str(row.ad_group_ad.ad.type_),
            "final_urls": list(row.ad_group_ad.ad.final_urls),
            "tracking_url_template": row.ad_group_ad.ad.tracking_url_template,
            "resource_name": row.ad_group_ad.resource_name,
            "headlines": headlines,
            "descriptions": descriptions
        }
        ads_found.append(ad_data)
        print(f"AdGroup: {row.ad_group.name} ({row.ad_group.id}) | Ad ID: {row.ad_group_ad.ad.id}")
        print(f"  Status: {row.ad_group_ad.status}")
        print(f"  Final URLs: {ad_data['final_urls']}")
        print(f"  Tracking Template: {ad_data['tracking_url_template']}")
        print(f"  Headlines: {headlines}")
        print(f"  Descriptions: {descriptions}")

with open("mintlify_ads_backup.json", "w", encoding="utf-8") as f:
    json.dump(ads_found, f, ensure_ascii=False, indent=2)

print(f"\nFound {len(ads_found)} ads in campaign {CAMPAIGN_ID}.")
