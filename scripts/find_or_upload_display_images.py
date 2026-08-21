import os
import requests
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def query_existing_images():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    q = """
        SELECT
            asset.id,
            asset.name,
            asset.resource_name,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.full_size.height_pixels
        FROM asset
        WHERE asset.type = 'IMAGE'
        ORDER BY asset.id DESC
        LIMIT 50
    """
    images = []
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            a = row.asset
            w = a.image_asset.full_size.width_pixels
            h = a.image_asset.full_size.height_pixels
            ratio = w / h if (w and h and h > 0) else 0
            images.append({
                "id": a.id,
                "name": a.name,
                "res": a.resource_name,
                "w": w,
                "h": h,
                "ratio": ratio
            })
            print(f"ID: {a.id:<15} | W: {w:<4} | H: {h:<4} | Ratio: {ratio:.2f} | Name: {a.name}")
    return images

def upload_image_asset(client, customer_id, name, img_url):
    print(f"Downloading image from: {img_url}")
    resp = requests.get(img_url, timeout=30)
    if resp.status_code != 200:
        raise ValueError(f"Failed to fetch image: {resp.status_code}")
    img_data = resp.content

    asset_service = client.get_service("AssetService")
    asset_op = client.get_type("AssetOperation")
    asset = asset_op.create
    asset.name = name
    asset.type_ = client.enums.AssetTypeEnum.IMAGE
    asset.image_asset.data = img_data

    mutate_resp = asset_service.mutate_assets(customer_id=customer_id, operations=[asset_op])
    created_res = mutate_resp.results[0].resource_name
    print(f"[SUCCESS] Uploaded asset '{name}': {created_res}")
    return created_res

if __name__ == '__main__':
    images = query_existing_images()
