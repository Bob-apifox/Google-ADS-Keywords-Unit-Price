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
            ad_group.id,
            ad_group.name,
            ad_group_ad.ad.id,
            ad_group_ad.ad.type,
            ad_group_ad.ad.final_url_suffix,
            ad_group_ad.ad.expanded_dynamic_search_ad.description,
            ad_group_ad.ad.expanded_dynamic_search_ad.description2,
            ad_group_ad.status
        FROM ad_group_ad
        WHERE campaign.name = 'Google-Sa-DSA-Alternatives-Global'
          AND ad_group_ad.status = 'ENABLED'
          AND ad_group.name LIKE 'DSA-%'
    """
    
    print("=== LIVE VERIFICATION OF 17 DSA ALTERNATIVES AD CREATIVES ===")
    results = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            ag_name = row.ad_group.name
            ad = row.ad_group_ad.ad
            if ag_name not in results:
                results[ag_name] = []
            results[ag_name].append({
                'ad_id': ad.id,
                'desc1': ad.expanded_dynamic_search_ad.description,
                'desc2': ad.expanded_dynamic_search_ad.description2,
                'suffix': ad.final_url_suffix
            })

    print(f"Total Configured DSA Groups with Active Ads: {len(results)}")
    for ag_name in sorted(results.keys()):
        ads = results[ag_name]
        print(f"\n[Ad Group] {ag_name} ({len(ads)} active ad)")
        for ad in ads:
            print(f"  ├─ Ad ID: {ad['ad_id']}")
            print(f"  ├─ Desc 1: {ad['desc1']}")
            print(f"  ├─ Desc 2: {ad['desc2']}")
            print(f"  └─ Tracking: {ad['suffix']}")

if __name__ == '__main__':
    main()
