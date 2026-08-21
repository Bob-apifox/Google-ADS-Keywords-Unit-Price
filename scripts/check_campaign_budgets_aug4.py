import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
customer_id = '9496728294'

campaign_names = [
    'Google-Sa-Swagger-Global',
    'Google-Sa-Mock-Global',
    'Google-Sa-Testing-Global'
]

# Query to get campaign budgets and recent metrics
query = """
    SELECT 
        campaign.name, 
        campaign.status, 
        campaign_budget.amount_micros,
        metrics.cost_micros,
        metrics.conversions
    FROM campaign 
    WHERE campaign.name IN ('Google-Sa-Swagger-Global', 'Google-Sa-Mock-Global', 'Google-Sa-Testing-Global')
      AND segments.date DURING LAST_7_DAYS
"""

try:
    stream = ga_service.search_stream(customer_id=customer_id, query=query)
    
    aggregated_data = {}
    
    for batch in stream:
        for row in batch.results:
            name = row.campaign.name
            if name not in aggregated_data:
                aggregated_data[name] = {
                    'budget': row.campaign_budget.amount_micros / 1000000 if row.campaign_budget else 0,
                    'cost': 0,
                    'conversions': 0
                }
            aggregated_data[name]['cost'] += row.metrics.cost_micros / 1000000
            aggregated_data[name]['conversions'] += row.metrics.conversions

    print("=== Campaign Budget & Performance Analysis (Last 7 Days) ===")
    for name in campaign_names:
        if name in aggregated_data:
            data = aggregated_data[name]
            print(f"Campaign: {name}")
            print(f"  - Current Daily Budget: ${data['budget']:.2f}")
            print(f"  - Cost (Last 7 days): ${data['cost']:.2f}")
            print(f"  - Conversions (Last 7 days): {data['conversions']}")
            print("-" * 50)
        else:
            print(f"Campaign: {name} (No data found in last 7 days)")
            print("-" * 50)

except Exception as e:
    print(f"Error executing query: {e}")
