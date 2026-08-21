import os
import sys
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
AD_GROUP_ID = "198612734597"  # API-Security-Testing ad group

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")
ad_group_ad_service = client.get_service("AdGroupAdService")
ad_group_service = client.get_service("AdGroupService")

# 1. Fetch existing ads in API-Security-Testing
query = f"""
    SELECT
        ad_group_ad.ad.id,
        ad_group_ad.resource_name
    FROM ad_group_ad
    WHERE ad_group.id = {AD_GROUP_ID}
      AND ad_group_ad.status != 'REMOVED'
"""

stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
remove_ops = []
for batch in stream:
    for row in batch.results:
        print(f"Removing existing Ad: {row.ad_group_ad.resource_name}")
        op = client.get_type("AdGroupAdOperation")
        op.remove = row.ad_group_ad.resource_name
        remove_ops.append(op)

if remove_ops:
    try:
        ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=remove_ops)
        print(f"SUCCESS: Removed {len(remove_ops)} old ads.")
    except Exception as e:
        print(f"Error removing old ads: {e}")

# 2. Create new RSA Ad with Updated Final URL: https://apidog.com/api-testing/
ag_path = ad_group_service.ad_group_path(CUSTOMER_ID, AD_GROUP_ID)
ad_op = client.get_type("AdGroupAdOperation")
ag_ad = ad_op.create
ag_ad.ad_group = ag_path
ag_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

rsa = ag_ad.ad.responsive_search_ad
headlines = [
    "API Security & Vulnerability",
    "OWASP API Top 10 Testing Tool",
    "Test JWT & Rate Limit Rules",
    "API Authentication Scanner",
    "DevSecOps API Security Testing",
    "Automated API Vulnerabilities",
    "Detect API BOLA & BFLA Flaws",
    "Validate API Auth Headers",
    "Secure Rest API Testing",
    "API Penetration Testing",
    "Continuous API Security",
    "Try Apidog Security Testing"
]
for hl in headlines:
    text_asset = client.get_type("AdTextAsset")
    text_asset.text = hl
    rsa.headlines.append(text_asset)

descriptions = [
    "Scan your APIs for OWASP Top 10 vulnerabilities, authentication bugs, and rate limits.",
    "Integrate API security checks directly into your developer workflow with zero setup.",
    "Detect broken object-level authorization (BOLA) and invalid tokens before deployment.",
    "All-in-one API testing platform with built-in security, schema validation & automated CI."
]
for desc in descriptions:
    text_asset = client.get_type("AdTextAsset")
    text_asset.text = desc
    rsa.descriptions.append(text_asset)

ag_ad.ad.final_urls.append("https://apidog.com/api-testing/")
ag_ad.ad.tracking_url_template = "{lpurl}?utm_source=google_search&utm_medium={network}&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

try:
    response = ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
    print(f"SUCCESS: Created new RSA Ad with updated Final URL https://apidog.com/api-testing/ ({response.results[0].resource_name})")
except Exception as e:
    print(f"Error creating updated RSA ad: {e}")
