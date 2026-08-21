import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

SITELINKS = [
    {
        "link_text": "1-Click Postman Migration",
        "desc1": "Import all your collections.",
        "desc2": "Migrate with zero data loss.",
        "url": "https://apidog.com/postman-migration"
    },
    {
        "link_text": "Visual API Design & Debug",
        "desc1": "Design, debug, and test.",
        "desc2": "Faster visual API tools.",
        "url": "https://apidog.com/api-debug"
    },
    {
        "link_text": "Enterprise Private Deploy",
        "desc1": "Local-first data privacy.",
        "desc2": "HIPAA compliant workspace.",
        "url": "https://apidog.com/siyouhua"
    },
    {
        "link_text": "Spec-First Development",
        "desc1": "Design APIs before code.",
        "desc2": "Keep docs & code in sync.",
        "url": "https://apidog.com/spec-first-mode"
    }
]

CALLOUTS = [
    "100% Offline Mode",
    "No Runner Limits",
    "1-Click Data Import",
    "Free Team Collaboration",
    "OpenAPI 3.1 Native"
]

def create_sitelink_asset(client, asset_service, sitelink_data):
    asset_op = client.get_type("AssetOperation")
    asset = asset_op.create
    asset.sitelink_asset.link_text = sitelink_data["link_text"]
    asset.sitelink_asset.description1 = sitelink_data["desc1"]
    asset.sitelink_asset.description2 = sitelink_data["desc2"]
    asset.final_urls.append(sitelink_data["url"])
    
    return asset_op

def create_callout_asset(client, asset_service, callout_text):
    asset_op = client.get_type("AssetOperation")
    asset = asset_op.create
    asset.callout_asset.callout_text = callout_text
    
    return asset_op

def execute_section3():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    asset_service = client.get_service("AssetService")
    customer_asset_service = client.get_service("CustomerAssetService")
    
    # 1. Create Assets (Sitelinks and Callouts)
    asset_operations = []
    
    for sl in SITELINKS:
        asset_operations.append(create_sitelink_asset(client, asset_service, sl))
        
    for co in CALLOUTS:
        asset_operations.append(create_callout_asset(client, asset_service, co))
        
    print(f"Creating {len(asset_operations)} Assets...")
    asset_response = asset_service.mutate_assets(
        customer_id=CUSTOMER_ID, operations=asset_operations
    )
    
    asset_resource_names = []
    for result in asset_response.results:
        asset_resource_names.append(result.resource_name)
        print(f"Created Asset: {result.resource_name}")
        
    # Sitelinks are the first 4, Callouts are the next 5
    sitelink_resources = asset_resource_names[:4]
    callout_resources = asset_resource_names[4:]
    
    # 2. Link Assets to Customer (Account Level)
    print("Linking Assets to Account (Customer Level)...")
    customer_asset_ops = []
    
    for res in sitelink_resources:
        op = client.get_type("CustomerAssetOperation")
        ca = op.create
        ca.asset = res
        ca.field_type = client.enums.AssetFieldTypeEnum.SITELINK
        customer_asset_ops.append(op)
        
    for res in callout_resources:
        op = client.get_type("CustomerAssetOperation")
        ca = op.create
        ca.asset = res
        ca.field_type = client.enums.AssetFieldTypeEnum.CALLOUT
        customer_asset_ops.append(op)
        
    ca_response = customer_asset_service.mutate_customer_assets(
        customer_id=CUSTOMER_ID, operations=customer_asset_ops
    )
    
    for result in ca_response.results:
        print(f"Created CustomerAsset link: {result.resource_name}")
        
    print("[SUCCESS] Account-level Ad Assets (Sitelinks & Callouts) successfully injected!")

if __name__ == '__main__':
    execute_section3()
