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
            asset.resource_name,
            asset.image_asset.full_size.width_pixels,
            asset.image_asset.full_size.height_pixels
        FROM asset
        WHERE asset.type = 'IMAGE'
    """
    landscapes = []
    squares = []
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            a = row.asset
            w = a.image_asset.full_size.width_pixels
            h = a.image_asset.full_size.height_pixels
            if not w or not h:
                continue
            ratio = w / h
            if 1.8 <= ratio <= 2.0:
                landscapes.append((a.id, a.name, w, h, a.resource_name))
            elif 0.95 <= ratio <= 1.05:
                squares.append((a.id, a.name, w, h, a.resource_name))

    print(f"Found {len(landscapes)} landscape (1.91:1) assets:")
    for l in landscapes[:10]:
        print(f"  ID: {l[0]} | {l[2]}x{l[3]} | Name: {l[1]}")

    print(f"\nFound {len(squares)} square (1:1) assets:")
    for s in squares[:10]:
        print(f"  ID: {s[0]} | {s[2]}x{s[3]} | Name: {s[1]}")

if __name__ == '__main__':
    main()
