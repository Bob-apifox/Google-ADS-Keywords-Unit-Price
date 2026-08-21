import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
customer_id = '9496728294'

# First query: get campaigns and their daily budgets
query_budget = """
    SELECT
        campaign.id,
        campaign.name,
        campaign.status,
        campaign_budget.amount_micros
    FROM campaign
    WHERE campaign.status = 'ENABLED'
    AND campaign.advertising_channel_type = 'SEARCH'
"""

response_budget = ga_service.search(customer_id=customer_id, query=query_budget)
campaigns = {}
for row in response_budget:
    camp_id = str(row.campaign.id)
    camp_name = row.campaign.name
    budget = row.campaign_budget.amount_micros / 1e6 if row.campaign_budget.amount_micros else 0
    campaigns[camp_id] = {'name': camp_name, 'budget': budget, 'spend_mtd': 0, 'spend_yesterday': 0}

# Second query: get total spend this month (July 2026)
query_spend_mtd = """
    SELECT
        campaign.id,
        metrics.cost_micros
    FROM campaign
    WHERE segments.month = '2026-07-01'
    AND campaign.status = 'ENABLED'
    AND campaign.advertising_channel_type = 'SEARCH'
"""
response_spend = ga_service.search(customer_id=customer_id, query=query_spend_mtd)
for row in response_spend:
    camp_id = str(row.campaign.id)
    if camp_id in campaigns:
        campaigns[camp_id]['spend_mtd'] = row.metrics.cost_micros / 1e6

# Third query: get spend for yesterday (July 29th, to see if they are currently throttled)
query_yesterday = """
    SELECT
        campaign.id,
        metrics.cost_micros
    FROM campaign
    WHERE segments.date = '2026-07-29'
    AND campaign.status = 'ENABLED'
    AND campaign.advertising_channel_type = 'SEARCH'
"""
response_yesterday = ga_service.search(customer_id=customer_id, query=query_yesterday)
for row in response_yesterday:
    camp_id = str(row.campaign.id)
    if camp_id in campaigns:
        campaigns[camp_id]['spend_yesterday'] = row.metrics.cost_micros / 1e6


print("=== Budget Pacing Analysis for July 2026 ===")
print("Checking for campaigns near their monthly limit (Budget * 30.4)")
print("-" * 110)
print(f"{'Campaign Name':<40} | {'Daily Budget':<12} | {'Monthly Cap':<12} | {'Spend MTD':<12} | {'Spend Yday':<12} | {'Status'}")
print("-" * 110)

throttled = []
healthy = []

for camp_id, data in campaigns.items():
    name = data['name']
    budget = data['budget']
    spend_mtd = data['spend_mtd']
    spend_yesterday = data['spend_yesterday']
    
    if budget == 0:
        continue
        
    monthly_cap = budget * 30.4
    spend_ratio = spend_mtd / monthly_cap if monthly_cap > 0 else 0
    
    # Identify throttled campaigns
    # If they've spent >90% of their monthly budget by July 29th (which is 29/31 = 93% of the month, so >90% is very tight)
    # OR if their yesterday spend is significantly lower than their daily budget despite having high MTD spend
    
    status = "OK"
    if spend_ratio >= 0.95:
        status = "⚠️ SEVERELY CAPPED"
        throttled.append(data)
    elif spend_ratio >= 0.85:
        if spend_yesterday < budget * 0.5:
            status = "⚠️ THROTTLED (Low Yday Spend)"
            throttled.append(data)
        else:
            status = "⚠️ NEARING CAP"
            throttled.append(data)
    elif spend_yesterday < budget * 0.2 and spend_mtd > budget * 10:
         status = "⚠️ SUSPICIOUS DROP"
         throttled.append(data)
    else:
        healthy.append(data)
        
    if status != "OK":
        print(f"{name[:38]:<40} | ${budget:<11.2f} | ${monthly_cap:<11.2f} | ${spend_mtd:<11.2f} | ${spend_yesterday:<11.2f} | {status}")

print("-" * 110)
print(f"\nFound {len(throttled)} campaigns with potential budget pacing constraints out of {len(campaigns)} active campaigns.")
