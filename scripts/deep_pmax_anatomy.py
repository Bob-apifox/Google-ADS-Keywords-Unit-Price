import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"
PMAX_CP_ID = "22341978472"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    print("==========================================================================")
    print("[1. PMAX CP-GLOBAL ASSET GROUP & ASSET TYPES AUDIT]")
    print("==========================================================================")
    
    # 1. Asset Group Details
    q_ag = f"""
        SELECT
            asset_group.id,
            asset_group.name,
            asset_group.status,
            asset_group.final_urls,
            asset_group.final_mobile_urls
        FROM asset_group
        WHERE campaign.id = {PMAX_CP_ID}
    """
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
        for row in batch.results:
            ag = row.asset_group
            print(f"Asset Group: {ag.name} (ID: {ag.id}, Status: {ag.status.name})")
            print(f"  Final URLs: {ag.final_urls}")

    # 2. Asset Group Assets (Headlines, Descriptions, Images, Videos)
    q_assets = f"""
        SELECT
            asset_group.name,
            asset.id,
            asset.name,
            asset.type,
            asset_group_asset.field_type,
            asset_group_asset.status
        FROM asset_group_asset
        WHERE campaign.id = {PMAX_CP_ID}
          AND asset_group_asset.status = 'ENABLED'
    """
    asset_types = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_assets):
        for row in batch.results:
            ft = row.asset_group_asset.field_type.name
            atype = row.asset.type_.name
            if ft not in asset_types:
                asset_types[ft] = []
            asset_types[ft].append((atype, row.asset.name))

    print(f"\nAssets Breakdown in Asset Group:")
    for ft, items in asset_types.items():
        print(f"  ├─ Field Type: {ft:<25} | Count: {len(items):<3}")

    # 3. Campaign Conversion Goals / Bidding
    q_camp = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.url_expansion_opt_out,
            campaign.selective_optimization.conversion_actions
        FROM campaign
        WHERE campaign.id = {PMAX_CP_ID}
    """
    print("\n--- Campaign Level Settings ---")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
        for row in batch.results:
            c = row.campaign
            print(f"URL Expansion Opt Out (Final URL Expansion Off?): {c.url_expansion_opt_out}")
            print(f"Selective Optimization Conversion Actions: {c.selective_optimization.conversion_actions}")

    # 4. Search Themes attached to Asset Group
    q_themes = f"""
        SELECT
            asset_group_signal.search_theme.text,
            asset_group_signal.audience.audience
        FROM asset_group_signal
        WHERE asset_group.id IN (SELECT asset_group.id FROM asset_group WHERE campaign.id = {PMAX_CP_ID})
    """
    print("\n--- Asset Group Search Themes / Audience Signals ---")
    try:
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_themes):
            for row in batch.results:
                st = row.asset_group_signal.search_theme.text
                aud = row.asset_group_signal.audience.audience
                if st:
                    print(f"  Search Theme: '{st}'")
                if aud:
                    print(f"  Audience: {aud}")
    except Exception as e:
        print(f"Signal query info: {e}")

if __name__ == '__main__':
    main()
