import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

client = GoogleAdsClient.load_from_storage(r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml")
customer_id = "9496728294"

ga_service = client.get_service("GoogleAdsService")

# Fetch last 7 days performance for all active campaigns
query = """
    SELECT campaign.id, campaign.name, metrics.cost_micros, metrics.conversions, campaign.campaign_budget
    FROM campaign
    WHERE campaign.status = 'ENABLED' 
      AND segments.date DURING LAST_7_DAYS
      AND metrics.cost_micros > 0
"""
try:
    response = ga_service.search(customer_id=customer_id, query=query)
    
    results = []
    for row in response:
        cost = row.metrics.cost_micros / 1000000.0
        convs = row.metrics.conversions
        cpa = cost / convs if convs > 0 else cost # If 0 convs, CPA is effectively the cost itself (wasted)
        
        # We also want the daily budget to know what we are reducing
        budget_id = row.campaign.campaign_budget.split('/')[-1]
        
        results.append({
            "name": row.campaign.name,
            "cost": cost,
            "convs": convs,
            "cpa": cpa,
            "budget_id": budget_id
        })
    
    # Sort by CPA descending (worst first)
    # Give priority to campaigns that spent a decent amount (e.g. > $20) with no conversions or high CPA
    results.sort(key=lambda x: (x['cpa'] if x['convs'] > 0 else x['cost'] + 999), reverse=True)
    
    print(f"{'Campaign Name':<50} | {'Cost':<8} | {'Convs':<6} | {'CPA':<8}")
    print("-" * 80)
    for r in results:
        # Highlight campaigns with CPA > $5 or Cost > $20 with 0 convs
        if (r['convs'] > 0 and r['cpa'] > 5.0) or (r['convs'] == 0 and r['cost'] > 20.0):
            print(f"! {r['name']:<47} | ${r['cost']:<7.2f} | {r['convs']:<6.1f} | ${r['cpa']:<7.2f}")
        else:
            print(f"  {r['name']:<47} | ${r['cost']:<7.2f} | {r['convs']:<6.1f} | ${r['cpa']:<7.2f}")
            
except Exception as e:
    print(f"Error: {e}")
