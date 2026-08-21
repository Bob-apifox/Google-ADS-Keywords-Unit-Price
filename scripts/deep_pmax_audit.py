import os
import requests
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

METABASE_URL = "https://metabase.apifox.cn/"
METABASE_USERNAME = "bob@apifox.com"
METABASE_PASSWORD = "08103245981Zgh"

def get_metabase_pmax_postman_history():
    session_res = requests.post(
        f"{METABASE_URL}api/session",
        json={"username": METABASE_USERNAME, "password": METABASE_PASSWORD},
        verify=False
    )
    session_id = session_res.json().get("id")
    headers = {"X-Metabase-Session": session_id}
    
    # Query last 14 days registrations for PMax Postman (23685533966) vs Search Postman (21982653330)
    sql = """
    SELECT
      DATE(`user_trackings`.`created_at`) AS `reg_date`,
      `user_trackings`.`utm_campaign` AS `utm_campaign`,
      COUNT(*) AS `count`
    FROM
      `user_trackings`
    WHERE
      `user_trackings`.`created_at` >= DATE(DATE_ADD(NOW(6), INTERVAL -14 day))
      AND (
        `user_trackings`.`utm_campaign` = '23685533966'
        OR `user_trackings`.`utm_campaign` = '21982653330'
        OR `user_trackings`.`utm_campaign` = '22341978472'
      )
    GROUP BY
      DATE(`user_trackings`.`created_at`),
      `user_trackings`.`utm_campaign`
    ORDER BY
      `reg_date` DESC
    """
    
    res = requests.post(
        f"{METABASE_URL}api/dataset",
        headers=headers,
        json={
            "database": 2, # Apidog RDS
            "type": "native",
            "native": {"query": sql}
        },
        verify=False
    )
    return res.json().get("data", {}).get("rows", [])

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    print("==========================================================================")
    print("[1. GOOGLE-PMAX-POSTMAN VS GOOGLE-SA-POSTMAN-GLOBAL 14-DAY PERFORMANCE]")
    print("==========================================================================")

    # Google Ads 14-day stats for PMax Postman and PMax CP-Global and Search Postman
    q_ads = """
        SELECT
            campaign.id,
            campaign.name,
            segments.date,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions
        FROM campaign
        WHERE campaign.id IN (23685533966, 21982653330, 22341978472)
          AND segments.date >= '2026-07-29'
          AND segments.date <= '2026-08-11'
        ORDER BY segments.date DESC
    """
    
    ads_stats = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ads):
        for row in batch.results:
            cid = str(row.campaign.id)
            cname = row.campaign.name
            dt = row.segments.date
            cost = row.metrics.cost_micros / 1000000.0
            clicks = row.metrics.clicks
            impr = row.metrics.impressions
            conv = row.metrics.conversions
            
            if cid not in ads_stats:
                ads_stats[cid] = {'name': cname, 'days': {}}
            ads_stats[cid]['days'][dt] = {
                'cost': cost, 'clicks': clicks, 'impr': impr, 'ads_conv': conv
            }

    # Merge with Metabase
    mb_rows = get_metabase_pmax_postman_history()
    mb_map = {}
    for r in mb_rows:
        dt_str = str(r[0])[:10]
        cid = str(r[1])
        cnt = r[2]
        if cid not in mb_map:
            mb_map[cid] = {}
        mb_map[cid][dt_str] = cnt

    print("\n--- Daily Comparison for Google-PMax-Postman (ID: 23685533966) ---")
    pmax_cost_total = 0
    pmax_regs_total = 0
    pmax_clicks_total = 0
    for dt, ddata in sorted(ads_stats.get('23685533966', {}).get('days', {}).items(), reverse=True):
        cost = ddata['cost']
        clicks = ddata['clicks']
        ads_conv = ddata['ads_conv']
        mb_reg = mb_map.get('23685533966', {}).get(dt, 0)
        cpr = f"${cost/mb_reg:.2f}" if mb_reg > 0 else "N/A"
        pmax_cost_total += cost
        pmax_regs_total += mb_reg
        pmax_clicks_total += clicks
        print(f"Date: {dt} | Spend: ${cost:<6.2f} | Clicks: {clicks:<4} | Ads Convs: {ads_conv:<4.1f} | Metabase Regs: {mb_reg:<3} | Real CPR: {cpr}")
    
    print(f"\n>> PMax-Postman 14-Day Totals: Spend: ${pmax_cost_total:.2f} | Clicks: {pmax_clicks_total} | DB Regs: {pmax_regs_total} | Real CPA: ${pmax_cost_total/pmax_regs_total if pmax_regs_total>0 else float('inf'):.2f}")

    print("\n--- PMax Placements Aggregated (Last 14 Days) ---")
    q_placements = """
        SELECT
            campaign.name,
            performance_max_placement_view.placement,
            performance_max_placement_view.placement_type,
            performance_max_placement_view.target_url,
            metrics.impressions
        FROM performance_max_placement_view
        WHERE campaign.id IN (23685533966, 22341978472)
          AND segments.date >= '2026-07-29'
          AND segments.date <= '2026-08-11'
        ORDER BY metrics.impressions DESC
        LIMIT 50
    """
    p_summary = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_placements):
        for row in batch.results:
            p = row.performance_max_placement_view.placement
            pt = row.performance_max_placement_view.placement_type.name
            impr = row.metrics.impressions
            cname = row.campaign.name
            if p not in p_summary:
                p_summary[p] = {'type': pt, 'impr': 0, 'camps': set()}
            p_summary[p]['impr'] += impr
            p_summary[p]['camps'].add(cname)

    print(f"Top 30 Aggregated PMax Placements (14-Day Impressions):")
    for p, pdata in sorted(p_summary.items(), key=lambda x: x[1]['impr'], reverse=True)[:30]:
        print(f"  [{pdata['type']:<15}] Impr: {pdata['impr']:<6} | Placement: {p} ({', '.join(pdata['camps'])})")

if __name__ == '__main__':
    main()
