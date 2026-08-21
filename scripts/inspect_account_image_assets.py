import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    q = """
        SELECT
            asset.id,
            asset.name,
            asset.type,
            asset.resource_name,
            asset.image_asset.file_size,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.full_size.height_pixels,
            asset.image_asset.full_size.url
        FROM asset
        WHERE asset.type = 'IMAGE'
        ORDER BY asset.id DESC
        LIMIT 30
    """
    print("=== ACCOUNT IMAGE ASSETS AUDIT ===")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            a = row.asset
            w = a.image_asset.full_size.width_pixels
            h = a.image_asset.full_size.height_pixels
            ratio = f"{w}x{h}" if w and h else "Unknown"
            print(f"Asset ID: {a.id:<15} | Name: {a.name:<35} | Dim: {ratio:<12} | URL: {a.image_asset.full_size.url}")

if __name__ == '__main__':
    main()
