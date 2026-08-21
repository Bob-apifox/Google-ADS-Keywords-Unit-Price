import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
customer_id = '9496728294'

def get_data_for_period(date_range_enum):
    query = f"""
        SELECT
            campaign.name,
            campaign.advertising_channel_type,
            metrics.cost_micros,
            metrics.conversions
        FROM campaign
        WHERE segments.date {date_range_enum}
        AND campaign.advertising_channel_type = 'SEARCH'
    """
    response = ga_service.search(customer_id=customer_id, query=query)
    data = {}
    for row in response:
        camp = row.campaign.name
        cost = row.metrics.cost_micros / 1e6
        conv = row.metrics.conversions
        data[camp] = {'cost': cost, 'conv': conv}
    return data

recent_data = get_data_for_period('DURING LAST_7_DAYS')
past_data = get_data_for_period('DURING LAST_14_DAYS')

previous_data = {}
for camp in past_data:
    p_cost = past_data[camp]['cost']
    p_conv = past_data[camp]['conv']
    r_cost = recent_data.get(camp, {}).get('cost', 0)
    r_conv = recent_data.get(camp, {}).get('conv', 0)
    
    prev_cost = p_cost - r_cost
    prev_conv = p_conv - r_conv
    previous_data[camp] = {'cost': prev_cost, 'conv': prev_conv}

print("=== Growth Analysis (Last 7 Days vs Previous 7 Days) ===")
print(f"{'Campaign':<40} | {'Recent Conv':<12} | {'Prev Conv':<12} | {'Growth':<10} | {'Recent CPA':<12} | {'Prev CPA':<12}")
print("-" * 105)

total_r_conv = 0
total_p_conv = 0
total_r_cost = 0
total_p_cost = 0

for camp in recent_data:
    r_conv = recent_data[camp]['conv']
    r_cost = recent_data[camp]['cost']
    p_conv = previous_data.get(camp, {}).get('conv', 0)
    p_cost = previous_data.get(camp, {}).get('cost', 0)
    
    total_r_conv += r_conv
    total_r_cost += r_cost
    total_p_conv += p_conv
    total_p_cost += p_cost
    
    if r_conv > 10 and r_conv > p_conv * 1.1: 
        growth = ((r_conv - p_conv) / p_conv * 100) if p_conv > 0 else 999
        r_cpa = r_cost / r_conv if r_conv > 0 else 0
        p_cpa = p_cost / p_conv if p_conv > 0 else 0
        print(f"{camp[:38]:<40} | {r_conv:<12.1f} | {p_conv:<12.1f} | +{growth:.1f}%   | ${r_cpa:<11.2f} | ${p_cpa:<11.2f}")

print("-" * 105)
r_cpa_total = total_r_cost / total_r_conv if total_r_conv > 0 else 0
p_cpa_total = total_p_cost / total_p_conv if total_p_conv > 0 else 0
growth_total = ((total_r_conv - total_p_conv) / total_p_conv * 100) if total_p_conv > 0 else 0
print(f"{'TOTAL SEARCH & DSA':<40} | {total_r_conv:<12.1f} | {total_p_conv:<12.1f} | +{growth_total:.1f}%   | ${r_cpa_total:<11.2f} | ${p_cpa_total:<11.2f}")
