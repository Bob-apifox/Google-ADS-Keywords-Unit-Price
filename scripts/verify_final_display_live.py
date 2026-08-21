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

    print("==================================================================================================")
    print("[LIVE VERIFICATION OF PMAX PAUSE & DISPLAY CAMPAIGNS (OFFICIAL GOOGLE ADS API)]")
    print("==================================================================================================")

    # 1. Campaigns Check
    q_c = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign_budget.amount_micros,
            campaign.target_cpa.target_cpa_micros
        FROM campaign
        WHERE campaign.name IN (
            'Google-PMax-CP-Global',
            'Google-Dis-Remarketing-Global',
            'Google-Dis-DevPlacements-Global'
        )
    """
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_c):
        for row in batch.results:
            c = row.campaign
            b = row.campaign_budget.amount_micros / 1000000.0
            tcpa = (c.target_cpa.target_cpa_micros or 0) / 1000000.0
            print(f"[{c.name:<32}] Type: {c.advertising_channel_type.name:<8} | Status: {c.status.name:<8} | Budget: ${b:<5.2f}/day | tCPA: ${tcpa:.2f}")

    # 2. Ad Groups & Targeting Check
    q_ag = """
        SELECT
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group.status,
            ad_group.optimized_targeting_enabled
        FROM ad_group
        WHERE campaign.name IN ('Google-Dis-Remarketing-Global', 'Google-Dis-DevPlacements-Global')
          AND ad_group.status != 'REMOVED'
    """
    print("\n--- AD GROUPS & TARGETING EXPANSION STATUS ---")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
        for row in batch.results:
            cname = row.campaign.name
            ag = row.ad_group
            print(f"[{cname:<32}] Ad Group: '{ag.name}' | Status: {ag.status.name} | Optimized Targeting: {ag.optimized_targeting_enabled}")

    # 3. Ads Check
    q_ad = """
        SELECT
            campaign.name,
            ad_group_ad.ad.id,
            ad_group_ad.status,
            ad_group_ad.ad.type
        FROM ad_group_ad
        WHERE campaign.name IN ('Google-Dis-Remarketing-Global', 'Google-Dis-DevPlacements-Global')
          AND ad_group_ad.status != 'REMOVED'
    """
    print("\n--- ACTIVE RDA DISPLAY CREATIVES ---")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ad):
        for row in batch.results:
            print(f"[{row.campaign.name:<32}] Ad ID: {row.ad_group_ad.ad.id} | Type: {row.ad_group_ad.ad.type_.name} | Status: {row.ad_group_ad.status.name}")

if __name__ == '__main__':
    main()
