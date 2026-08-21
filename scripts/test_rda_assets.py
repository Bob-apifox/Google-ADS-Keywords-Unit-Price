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
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")

    q = """
        SELECT
            asset.id,
            asset.name,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.full_size.height_pixels,
            asset.image_asset.file_size
        FROM asset
        WHERE asset.id IN (183793374610, 188645331605, 183756328178, 183756508835, 342769458841)
    """
    for batch in ga_service.search_stream(customer_id=customer_id, query=q):
        for row in batch.results:
            a = row.asset
            w = a.image_asset.full_size.width_pixels
            h = a.image_asset.full_size.height_pixels
            size = a.image_asset.file_size
            print(f"Asset: {a.id} | {w}x{h} | Size: {size} bytes | Name: {a.name}")

if __name__ == '__main__':
    main()
