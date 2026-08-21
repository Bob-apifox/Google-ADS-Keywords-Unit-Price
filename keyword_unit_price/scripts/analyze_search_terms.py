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
      search_term_view.search_term,
      campaign.name,
      metrics.clicks,
      metrics.cost_micros
    FROM search_term_view
    WHERE segments.date DURING LAST_7_DAYS
      AND metrics.clicks > 0
    ORDER BY metrics.cost_micros DESC
    LIMIT 200
"""

response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
terms = []
for row in response:
    term = row.search_term_view.search_term.lower()
    cost = row.metrics.cost_micros / 1000000
    clicks = row.metrics.clicks
    terms.append({'term': term, 'cost': cost, 'clicks': clicks, 'campaign': row.campaign.name})

flagged_terms = []
suspicious_words = [
    'free', 'crack', 'download', 'tutorial', 'how to', 'login', 
    'error', 'job', 'salary', 'interview', 'student', 'course', 
    'github', 'reddit', 'app', 'android', 'ios', 'weather', 'pokemon',
    'open source', 'offline', 'vs', 'vs code', 'extension', 'plugin',
    'python', 'java', 'c#', 'react', 'vue', 'angular', 'course', 'learn'
]

for t in terms:
    is_suspicious = False
    for word in suspicious_words:
        if word in t['term'].split():
            is_suspicious = True
            break
    if is_suspicious:
        flagged_terms.append(t)

print("--- Suspicious Search Terms (Last 7 Days) ---")
for t in flagged_terms:
    print(f"Term: '{t['term']}' | Cost: ${t['cost']:.2f} | Clicks: {t['clicks']} | Campaign: {t['campaign']}")

print("\n--- Top 30 Costliest Terms (Unfiltered) ---")
for t in terms[:30]:
    print(f"Term: '{t['term']}' | Cost: ${t['cost']:.2f} | Clicks: {t['clicks']} | Campaign: {t['campaign']}")
