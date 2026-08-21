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
            ad_group.id,
            ad_group.name,
            ad_group.status,
            metrics.cost_micros,
            metrics.clicks,
            metrics.conversions
        FROM ad_group
        WHERE campaign.name IN ('Google-Sa-Comp-HeavyQA-Global', 'Google-Sa-Func-ContractTest-Global')
          AND segments.date BETWEEN '2026-08-03' AND '2026-08-10'
    """
    
    print("=== Checking Google-Sa-Comp-HeavyQA-Global & Google-Sa-Func-ContractTest-Global ===")
    results = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            cname = row.campaign.name
            cid = row.campaign.id
            ag_name = row.ad_group.name
            ag_id = row.ad_group.id
            ag_status = row.ad_group.status.name
            c = row.metrics.cost_micros / 1000000.0
            clicks = row.metrics.clicks
            conv = row.metrics.conversions
            
            key = f"{cname} ({cid})"
            if key not in results: results[key] = {}
            if ag_name not in results[key]:
                results[key][ag_name] = {'id': ag_id, 'status': ag_status, 'cost': 0.0, 'clicks': 0, 'convs': 0.0}
            results[key][ag_name]['cost'] += c
            results[key][ag_name]['clicks'] += clicks
            results[key][ag_name]['convs'] += conv

    for ckey, ags in results.items():
        print(f"\n[Campaign] {ckey}")
        for ag_name, d in ags.items():
            cpa = d['cost'] / d['convs'] if d['convs'] > 0 else 0.0
            print(f"   [Ad Group] {ag_name:<30} (ID: {d['id']}) | Status: {d['status']} | Cost: ${d['cost']:<6.2f} | Clicks: {d['clicks']:<4} | Convs: {d['convs']:<5.1f} | CPA: ${cpa:.2f}")

if __name__ == '__main__':
    main()
