import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'
AD_GROUP_ID = '203616129528'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ad_group_ad_service = client.get_service('AdGroupAdService')
ad_group_service = client.get_service('AdGroupService')

tracking_url_template = "{lpurl}?utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term=dsa-vs-competitor"

print("Creating Dynamic Search Ads...")
ad_ops = []

# Ad 1
op1 = client.get_type("AdGroupAdOperation")
ad_group_ad1 = op1.create
ad_group_ad1.ad_group = ad_group_service.ad_group_path(CUSTOMER_ID, AD_GROUP_ID)
ad_group_ad1.status = client.enums.AdGroupAdStatusEnum.ENABLED
ad1 = ad_group_ad1.ad
ad1.tracking_url_template = tracking_url_template
ad1.expanded_dynamic_search_ad.description = "Looking for a better API alternative? Switch to Apidog for a faster, modern workflow."
ad1.expanded_dynamic_search_ad.description2 = "Import all your existing API data in 1-click. Join 1,000,000+ developers today."
ad_ops.append(op1)

# Ad 2
op2 = client.get_type("AdGroupAdOperation")
ad_group_ad2 = op2.create
ad_group_ad2.ad_group = ad_group_service.ad_group_path(CUSTOMER_ID, AD_GROUP_ID)
ad_group_ad2.status = client.enums.AdGroupAdStatusEnum.ENABLED
ad2 = ad_group_ad2.ad
ad2.tracking_url_template = tracking_url_template
ad2.expanded_dynamic_search_ad.description = "Stop paying for overpriced API tools. Apidog offers more powerful features for free."
ad2.expanded_dynamic_search_ad.description2 = "Experience seamless API Design, Debugging, Mocking and Testing in one unified platform."
ad_ops.append(op2)

try:
    response = ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=ad_ops)
    for result in response.results:
        print(f"Success: Created Ad {result.resource_name}")
except Exception as e:
    print(f"Error creating ads: {e}")

print("DONE.")
