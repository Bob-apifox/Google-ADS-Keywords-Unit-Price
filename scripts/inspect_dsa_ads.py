import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

# Check what existing ads are in Google-Sa-DSA-Alternatives-Global
def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    q = """
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group_ad.ad.id,
            ad_group_ad.ad.type,
            ad_group_ad.ad.expanded_dynamic_search_ad.description,
            ad_group_ad.ad.expanded_dynamic_search_ad.description2,
            ad_group_ad.status
        FROM ad_group_ad
        WHERE campaign.name = 'Google-Sa-DSA-Alternatives-Global'
    """
    
    print("=== CHECKING ADS IN DSA CAMPAIGN ===")
    found = 0
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            found += 1
            ag = row.ad_group
            ad = row.ad_group_ad.ad
            print(f"AG: {ag.name:<30} | Ad ID: {ad.id} | Type: {ad.type_.name} | Status: {row.ad_group_ad.status.name}")
            if ad.expanded_dynamic_search_ad:
                print(f"   Desc 1: {ad.expanded_dynamic_search_ad.description}")
                print(f"   Desc 2: {ad.expanded_dynamic_search_ad.description2}")

    print(f"\nTotal Ads found in DSA campaign: {found}")

if __name__ == '__main__':
    main()
