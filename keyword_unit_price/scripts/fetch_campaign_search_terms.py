import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")

query = """
    SELECT
      campaign.id,
      campaign.name,
      search_term_view.search_term,
      metrics.clicks,
      metrics.cost_micros
    FROM search_term_view
    WHERE segments.date DURING LAST_7_DAYS
      AND metrics.clicks > 0
    ORDER BY metrics.cost_micros DESC
    LIMIT 2000
"""

response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

campaign_terms = {}

for row in response:
    c_name = row.campaign.name
    term = row.search_term_view.search_term.lower()
    cost = row.metrics.cost_micros / 1000000
    clicks = row.metrics.clicks
    
    if c_name not in campaign_terms:
        campaign_terms[c_name] = []
    
    campaign_terms[c_name].append({'term': term, 'cost': cost, 'clicks': clicks})

print("==========================================")
output_file = 'd:/Apidog Work/Google ADS Keywords Unit Price/keyword_unit_price/reports/campaign_search_terms.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("==========================================\n")
    f.write("TOP SEARCH TERMS PER CAMPAIGN (Last 7 Days)\n")
    f.write("==========================================\n\n")
    for c_name, terms in campaign_terms.items():
        f.write(f"[{c_name}]\n")
        for t in terms[:15]:
            f.write(f"  - {t['term']} (Cost: ${t['cost']:.2f}, Clicks: {t['clicks']})\n")
        f.write("\n")
print(f"Output saved to {output_file}")

