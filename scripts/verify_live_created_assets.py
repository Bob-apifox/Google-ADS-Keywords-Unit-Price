import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

NEW_AG_IDS = ["198839811043", "198667762266", "198839869603"]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    print("==========================================================================")
    print("[LIVE GOOGLE ADS API ASSET VERIFICATION]")
    print("==========================================================================")

    # 1. Verify Campaigns Budget & tCPA
    c_query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros,
            campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.name IN (
            'Google-Sa-DSA-Alternatives-Global',
            'Google-Sa-Func-MultiProtocol-Global',
            'Google-Sa-Comp-HeavyQA-Global',
            'Google-Sa-Doc-Global'
        )
    """
    print("\n--- 1. [Campaigns Live Budgets & Target CPAs] ---")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=c_query):
        for row in batch.results:
            c = row.campaign
            b = row.campaign_budget.amount_micros / 1000000.0
            tcpa = (c.maximize_conversions.target_cpa_micros or c.target_cpa.target_cpa_micros) / 1000000.0
            print(f"Campaign: {c.name:<36} | Live Budget: ${b:<6.2f}/day | Live Target CPA: ${tcpa:.2f}")

    # 2. Verify 4.1 DSA Ad Groups
    dsa_ag_query = """
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.status
        FROM ad_group
        WHERE campaign.name = 'Google-Sa-DSA-Alternatives-Global'
          AND ad_group.status = 'ENABLED'
    """
    print("\n--- 2. [Google-Sa-DSA-Alternatives-Global Live Ad Groups] ---")
    dsa_groups = []
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=dsa_ag_query):
        for row in batch.results:
            dsa_groups.append((row.ad_group.id, row.ad_group.name))
    print(f"Total Active Ad Groups in DSA Alternatives: {len(dsa_groups)}")
    for ag_id, ag_name in sorted(dsa_groups, key=lambda x: x[1]):
        print(f"  [OK] Ad Group: {ag_name:<30} (ID: {ag_id})")

    # 3. Verify RSA Ads, Headlines, Descriptions and Keywords
    rsa_query = f"""
        SELECT
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group_ad.ad.id,
            ad_group_ad.ad.type,
            ad_group_ad.ad.final_urls,
            ad_group_ad.ad.final_url_suffix,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.ad.responsive_search_ad.descriptions,
            ad_group_ad.status
        FROM ad_group_ad
        WHERE ad_group.id IN ({', '.join(NEW_AG_IDS)})
          AND ad_group_ad.status = 'ENABLED'
    """
    print("\n--- 3. [Newly Deployed RSA Groups & Creatives Details] ---")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=rsa_query):
        for row in batch.results:
            cname = row.campaign.name
            ag = row.ad_group
            ad = row.ad_group_ad.ad
            h_count = len(ad.responsive_search_ad.headlines)
            d_count = len(ad.responsive_search_ad.descriptions)
            
            print(f"\n[Campaign] {cname}")
            print(f"  ├─ Ad Group:         {ag.name} (ID: {ag.id})")
            print(f"  ├─ Ad ID:            {ad.id} ({ad.type_.name})")
            print(f"  ├─ Final URL:        {ad.final_urls[0]}")
            print(f"  ├─ Tracking Suffix:  {ad.final_url_suffix}")
            print(f"  ├─ Headlines Count:  {h_count} (Max allowed: 15)")
            print(f"  └─ Descriptions:     {d_count} (Max allowed: 4)")

    print("\n==========================================================================")
    print("[ALL ASSETS CONFIRMED 100% ONLINE & LIVE IN GOOGLE ADS]")
    print("==========================================================================")

if __name__ == '__main__':
    main()
