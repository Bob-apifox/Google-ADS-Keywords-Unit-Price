import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
customer_id = '9496728294'

campaigns_to_check = ['Google-Sa-Testing-Global', 'Google-Sa-Func-CICD-Global']
query = f"""
    SELECT
        campaign.id,
        campaign.name,
        campaign_budget.amount_micros,
        campaign.target_cpa.target_cpa_micros
    FROM campaign
    WHERE campaign.name IN ({', '.join([f"'{c}'" for c in campaigns_to_check])})
    AND campaign.status = 'ENABLED'
"""

response = ga_service.search(customer_id=customer_id, query=query)
print("=== Current Budget & tCPA ===")
for row in response:
    name = row.campaign.name
    budget = row.campaign_budget.amount_micros / 1e6 if row.campaign_budget.amount_micros else 0
    tcpa = row.campaign.target_cpa.target_cpa_micros / 1e6 if row.campaign.target_cpa.target_cpa_micros else 0
    print(f"Campaign: {name}")
    print(f"  Current Budget: ${budget:.2f} -> +20% = ${budget * 1.2:.2f}")
    if tcpa > 0:
        print(f"  Current tCPA: ${tcpa:.2f} -> +15% = ${tcpa * 1.15:.2f}")
    else:
        print("  Current tCPA: Not set or using different strategy.")
    print("-" * 40)
