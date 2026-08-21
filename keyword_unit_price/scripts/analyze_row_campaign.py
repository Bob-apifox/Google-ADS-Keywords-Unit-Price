import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")

campaign_name = "Google-Sa-CP-ROW-MultiLang"

print(f"Analyzing Campaign: {campaign_name}")

query_camp = f"""
    SELECT
        campaign.id,
        campaign.name,
        campaign.status,
        campaign.serving_status,
        campaign.bidding_strategy_type,
        campaign.target_cpa.target_cpa_micros,
        campaign.maximize_conversions.target_cpa_micros,
        campaign_budget.amount_micros,
        campaign_budget.status,
        campaign.optimization_score
    FROM campaign
    WHERE campaign.name = '{campaign_name}'
"""
response = ga_service.search(customer_id=CUSTOMER_ID, query=query_camp)
campaign_id = None
for row in response:
    campaign_id = row.campaign.id
    print("--- Campaign Info ---")
    print(f"ID: {row.campaign.id}")
    print(f"Status: {row.campaign.status.name}")
    print(f"Serving Status: {row.campaign.serving_status.name}")
    print(f"Bidding Strategy Type: {row.campaign.bidding_strategy_type.name}")
    
    tCPA = None
    if row.campaign.target_cpa.target_cpa_micros:
        tCPA = row.campaign.target_cpa.target_cpa_micros / 1000000
    if row.campaign.maximize_conversions.target_cpa_micros:
        tCPA = row.campaign.maximize_conversions.target_cpa_micros / 1000000
        
    print(f"Target CPA: ${tCPA if tCPA else 'Not set'}")
    print(f"Budget: ${row.campaign_budget.amount_micros / 1000000 if row.campaign_budget.amount_micros else 'N/A'}")

if not campaign_id:
    print("Campaign not found.")
    exit()

query_ag = f"""
    SELECT
        ad_group.id,
        ad_group.name,
        ad_group.status,
        ad_group.target_cpa_micros
    FROM ad_group
    WHERE campaign.id = {campaign_id}
"""
print("\n--- Ad Groups ---")
response_ag = ga_service.search(customer_id=CUSTOMER_ID, query=query_ag)
ag_count = 0
for row in response_ag:
    ag_count += 1
    tCPA_ag = row.ad_group.target_cpa_micros / 1000000 if row.ad_group.target_cpa_micros else "Inherited"
    print(f"- {row.ad_group.name} (Status: {row.ad_group.status.name}) - AdGroup tCPA: {tCPA_ag}")
print(f"Total Ad Groups: {ag_count}")

query_kw = f"""
    SELECT
        ad_group_criterion.keyword.text,
        ad_group_criterion.status,
        ad_group_criterion.system_serving_status,
        ad_group_criterion.approval_status
    FROM ad_group_criterion
    WHERE campaign.id = {campaign_id}
      AND ad_group_criterion.type = 'KEYWORD'
      AND ad_group_criterion.status = 'ENABLED'
"""
print("\n--- Keywords Diagnostics ---")
response_kw = ga_service.search(customer_id=CUSTOMER_ID, query=query_kw)
kw_count = 0
low_search_volume_count = 0
for row in response_kw:
    kw_count += 1
    if row.ad_group_criterion.system_serving_status.name == 'RARELY_SERVED':
        low_search_volume_count += 1
        
print(f"Total Enabled Keywords: {kw_count}")
print(f"Keywords with 'Low Search Volume' (RARELY_SERVED): {low_search_volume_count}")

query_ad = f"""
    SELECT
        ad_group_ad.ad.id,
        ad_group_ad.status,
        ad_group_ad.policy_summary.approval_status
    FROM ad_group_ad
    WHERE campaign.id = {campaign_id}
      AND ad_group_ad.status = 'ENABLED'
"""
print("\n--- Ads Diagnostics ---")
response_ad = ga_service.search(customer_id=CUSTOMER_ID, query=query_ad)
ad_count = 0
disapproved_count = 0
limited_count = 0
for row in response_ad:
    ad_count += 1
    status = row.ad_group_ad.policy_summary.approval_status.name
    if status == 'DISAPPROVED':
        disapproved_count += 1
    elif status == 'APPROVED_LIMITED':
        limited_count += 1

print(f"Total Enabled Ads: {ad_count}")
print(f"Disapproved Ads: {disapproved_count}")
print(f"Approved (Limited) Ads: {limited_count}")
