import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")

print("Fetching all ENABLED campaigns...")

query_all = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.bidding_strategy_type,
        campaign.target_cpa.target_cpa_micros,
        campaign.maximize_conversions.target_cpa_micros,
        campaign.serving_status
    FROM campaign
    WHERE campaign.status = 'ENABLED'
"""
res_all = ga_service.search(customer_id=CUSTOMER_ID, query=query_all)
campaigns = {}
for row in res_all:
    c_id = row.campaign.id
    # Skip newly created Phase 3 campaigns
    if row.campaign.name.startswith("Google-Sa-Comp-") or row.campaign.name.startswith("Google-Sa-Func-"):
        continue
    # Skip the one we just fixed
    if row.campaign.name == "Google-Sa-CP-ROW-MultiLang":
        continue
        
    tCPA = None
    if row.campaign.target_cpa.target_cpa_micros:
        tCPA = row.campaign.target_cpa.target_cpa_micros / 1000000
    if row.campaign.maximize_conversions.target_cpa_micros:
        tCPA = row.campaign.maximize_conversions.target_cpa_micros / 1000000
        
    campaigns[c_id] = {
        'name': row.campaign.name,
        'bidding_strategy': row.campaign.bidding_strategy_type.name,
        'serving_status': row.campaign.serving_status.name,
        'tCPA': tCPA,
        'cost': 0
    }

print("Fetching cost data for the last 7 days...")
query_metrics = """
    SELECT
        campaign.id,
        metrics.cost_micros
    FROM campaign
    WHERE campaign.status = 'ENABLED'
      AND segments.date DURING LAST_7_DAYS
"""
res_metrics = ga_service.search(customer_id=CUSTOMER_ID, query=query_metrics)
for row in res_metrics:
    c_id = row.campaign.id
    if c_id in campaigns:
        campaigns[c_id]['cost'] += row.metrics.cost_micros

zero_spend = [c_id for c_id, data in campaigns.items() if data['cost'] == 0]

print(f"\nFound {len(zero_spend)} old ENABLED campaigns with $0 spend in the last 7 days.")

for c_id in zero_spend:
    c_data = campaigns[c_id]
    print(f"\n=====================================")
    print(f"Campaign: {c_data['name']}")
    print(f"Strategy: {c_data['bidding_strategy']}, Target CPA: ${c_data['tCPA'] if c_data['tCPA'] else 'None'}")
    
    query_ad = f"""
        SELECT ad_group_ad.policy_summary.approval_status
        FROM ad_group_ad
        WHERE campaign.id = {c_id} AND ad_group_ad.status = 'ENABLED'
    """
    total_ads = 0
    disapproved = 0
    try:
        res_ad = ga_service.search(customer_id=CUSTOMER_ID, query=query_ad)
        for r in res_ad:
            total_ads += 1
            if r.ad_group_ad.policy_summary.approval_status.name == 'DISAPPROVED':
                disapproved += 1
        print(f"Ads: {total_ads} enabled, {disapproved} disapproved.")
    except Exception as e:
        pass

    query_kw = f"""
        SELECT ad_group_criterion.system_serving_status
        FROM ad_group_criterion
        WHERE campaign.id = {c_id} AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD'
    """
    total_kw = 0
    low_volume = 0
    try:
        res_kw = ga_service.search(customer_id=CUSTOMER_ID, query=query_kw)
        for r in res_kw:
            total_kw += 1
            if r.ad_group_criterion.system_serving_status.name == 'RARELY_SERVED':
                low_volume += 1
        print(f"Keywords: {total_kw} enabled, {low_volume} low search volume.")
    except Exception as e:
        pass
        
    print(f"Likely Reason:")
    if total_ads == 0:
        print("-> NO ENABLED ADS. Campaign has nothing to show.")
    elif total_kw > 0 and low_volume == total_kw:
        print("-> LOW SEARCH VOLUME. All keywords are marked as rarely served.")
    elif disapproved > 0 and disapproved == total_ads:
        print("-> POLICY DISAPPROVAL. All ads are disapproved.")
    elif c_data['tCPA'] is not None and c_data['tCPA'] <= 2.5:
        print(f"-> EXTREMELY LOW tCPA (${c_data['tCPA']}). Algorithm skipping auctions.")
    else:
        print("-> Needs manual inspection. Could be bid limits, small audience, or ad group status.")
