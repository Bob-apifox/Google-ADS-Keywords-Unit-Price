import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_budget.amount_micros,
            segments.date,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions
        FROM campaign
        WHERE campaign.name LIKE '%DSA%'
          AND segments.date BETWEEN '2026-08-03' AND '2026-08-10'
    """
    
    print("=== Querying DSA Campaigns Performance (2026-08-03 to 2026-08-10) ===")
    camp_data = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            cid = str(row.campaign.id)
            name = row.campaign.name
            if name not in camp_data:
                camp_data[name] = {'cost': 0.0, 'clicks': 0, 'impressions': 0, 'conversions': 0.0, 'budget': row.campaign_budget.amount_micros / 1000000.0}
            camp_data[name]['cost'] += row.metrics.cost_micros / 1000000.0
            camp_data[name]['clicks'] += row.metrics.clicks
            camp_data[name]['impressions'] += row.metrics.impressions
            camp_data[name]['conversions'] += row.metrics.conversions

    print(f"{'Campaign Name':<40} | {'Budget/Day':<12} | {'Total Cost':<12} | {'Clicks':<8} | {'Conversions':<12} | {'CPA (USD)':<10}")
    print('-'*105)
    for name, d in camp_data.items():
        cpa = d['cost'] / d['conversions'] if d['conversions'] > 0 else 0.0
        print(f"{name:<40} | ${d['budget']:<11.2f} | ${d['cost']:<11.2f} | {d['clicks']:<8} | {d['conversions']:<12.1f} | ${cpa:<9.2f}")

    # Let's also check Ad Group level for Google-Sa-DSA-Alternatives-Global
    ag_query = """
        SELECT
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group.status,
            metrics.cost_micros,
            metrics.clicks,
            metrics.conversions
        FROM ad_group
        WHERE campaign.name = 'Google-Sa-DSA-Alternatives-Global'
          AND segments.date BETWEEN '2026-08-03' AND '2026-08-10'
    """
    print("\n=== Ad Groups in Google-Sa-DSA-Alternatives-Global ===")
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=ag_query):
        for row in batch.results:
            c = row.metrics.cost_micros / 1000000.0
            conv = row.metrics.conversions
            cpa = c / conv if conv > 0 else 0.0
            print(f"Ad Group: {row.ad_group.name} | Status: {row.ad_group.status.name} | Cost: ${c:.2f} | Clicks: {row.metrics.clicks} | Convs: {conv:.1f} | CPA: ${cpa:.2f}")

if __name__ == '__main__':
    main()
