import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

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
CAMPAIGN_ID = "23320166856"  # Google-Sa-Mintlify-Global

TARGET_BASE_URL = "https://apidog.com/compare/apidog-vs-mintlify/"
TARGET_FINAL_URL = f"{TARGET_BASE_URL}?utm_source=google_search&utm_medium=ads_sa&utm_campaign={{campaignid}}&utm_content={{adgroupid}}&utm_term={{keyword}}"

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")
ad_group_ad_service = client.get_service("AdGroupAdService")
ad_service = client.get_service("AdService")

query = f"""
    SELECT
        campaign.id,
        campaign.name,
        ad_group.id,
        ad_group.name,
        ad_group_ad.ad.id,
        ad_group_ad.ad.final_urls,
        ad_group_ad.status
    FROM ad_group_ad
    WHERE campaign.id = {CAMPAIGN_ID}
      AND ad_group_ad.status != 'REMOVED'
"""

stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)

operations = []
for batch in stream:
    for row in batch.results:
        ad_id = row.ad_group_ad.ad.id
        ad_group_id = row.ad_group.id
        current_urls = list(row.ad_group_ad.ad.final_urls)
        
        print(f"Checking Ad {ad_id} in AdGroup '{row.ad_group.name}' ({ad_group_id}) | Current URLs: {current_urls}")
        
        # Check if URL needs update
        needs_update = False
        if not current_urls or TARGET_BASE_URL not in current_urls[0]:
            needs_update = True

        if needs_update:
            op = client.get_type("AdGroupAdOperation")
            ad_group_ad = op.update
            ad_group_ad.resource_name = ad_group_ad_service.ad_group_ad_path(CUSTOMER_ID, ad_group_id, ad_id)
            ad_group_ad.ad.resource_name = ad_service.ad_path(CUSTOMER_ID, ad_id)
            
            # Clear old final_urls and add new
            del ad_group_ad.ad.final_urls[:]
            ad_group_ad.ad.final_urls.append(TARGET_FINAL_URL)
            
            client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, ad_group_ad._pb))
            operations.append(op)

if operations:
    print(f"\nUpdating {len(operations)} ads to {TARGET_FINAL_URL}...")
    try:
        response = ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=operations)
        print(f"SUCCESS: Updated {len(response.results)} ads.")
    except Exception as e:
        print(f"Error updating ads: {e}")
else:
    print(f"\nAll active ads in campaign {CAMPAIGN_ID} already have the target URL.")
