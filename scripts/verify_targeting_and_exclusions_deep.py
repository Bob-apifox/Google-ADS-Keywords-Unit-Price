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

    print("==========================================================================")
    print("[1. AUDITING TRACK 1: Google-Dis-Remarketing-Global (24126382470)]")
    print("==========================================================================")

    # 1. Ad Group level criteria
    q_ag_c1 = """
        SELECT
            ad_group_criterion.criterion_id,
            ad_group_criterion.type,
            ad_group_criterion.user_list.user_list,
            ad_group_criterion.status
        FROM ad_group_criterion
        WHERE campaign.id = 24126382470
    """
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag_c1):
        for row in batch.results:
            c = row.ad_group_criterion
            print(f"  Ad Group Target: Type={c.type_.name} | UserList={c.user_list.user_list} | Status={c.status.name}")

    # Campaign level exclusions
    q_camp_c1 = """
        SELECT
            campaign_criterion.criterion_id,
            campaign_criterion.type,
            campaign_criterion.negative,
            campaign_criterion.user_list.user_list
        FROM campaign_criterion
        WHERE campaign.id = 24126382470
    """
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp_c1):
        for row in batch.results:
            cc = row.campaign_criterion
            print(f"  Campaign Exclusion: Negative={cc.negative} | Type={cc.type_.name} | UserList={cc.user_list.user_list}")

    print("\n==========================================================================")
    print("[2. AUDITING TRACK 2: Google-Dis-DevPlacements-Global (24131994659)]")
    print("==========================================================================")

    # Ad Group level placements
    q_ag_c2 = """
        SELECT
            ad_group_criterion.criterion_id,
            ad_group_criterion.type,
            ad_group_criterion.placement.url,
            ad_group_criterion.status
        FROM ad_group_criterion
        WHERE campaign.id = 24131994659
    """
    placements = []
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag_c2):
        for row in batch.results:
            c = row.ad_group_criterion
            if c.placement.url:
                placements.append(c.placement.url)
    print(f"  Whitelisted Placements Count: {len(placements)}")
    for p in placements:
        print(f"    - {p}")

    # Campaign level exclusions
    q_camp_c2 = """
        SELECT
            campaign_criterion.criterion_id,
            campaign_criterion.type,
            campaign_criterion.negative,
            campaign_criterion.placement.url,
            campaign_criterion.content_label.type
        FROM campaign_criterion
        WHERE campaign.id = 24131994659
    """
    print("\n  Campaign Exclusions:")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp_c2):
        for row in batch.results:
            cc = row.campaign_criterion
            print(f"    Type={cc.type_.name} | Negative={cc.negative} | Placement={cc.placement.url} | ContentLabel={cc.content_label.type_.name if cc.content_label else ''}")

if __name__ == '__main__':
    main()
