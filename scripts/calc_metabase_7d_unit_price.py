import os
import requests
from google.ads.googleads.client import GoogleAdsClient
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

METABASE_URL = "https://metabase.apifox.cn/"
METABASE_USERNAME = "bob@apifox.com"
METABASE_PASSWORD = "08103245981Zgh"
GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def get_metabase_7d():
    session_res = requests.post(f"{METABASE_URL}api/session", json={
        "username": METABASE_USERNAME, 
        "password": METABASE_PASSWORD
    }, verify=False)
    session_id = session_res.json().get("id")
    headers = {"X-Metabase-Session": session_id}
    
    db_res = requests.get(f"{METABASE_URL}api/database", headers=headers, verify=False)
    db_id = 2
    for db in db_res.json().get("data", []):
        if "api_development" in db.get("name", "").lower() or "production" in db.get("name", "").lower():
            db_id = db["id"]
            break

    # Last 7 Days (2026-08-03 to 2026-08-09 inclusive)
    sql_7d = """
    SELECT
      `user_trackings`.`utm_campaign` AS `utm_campaign`,
      COUNT(*) AS `count`
    FROM
      `user_trackings`
    WHERE
      `user_trackings`.`created_at` >= '2026-08-03 00:00:00'
      AND `user_trackings`.`created_at` <= '2026-08-09 23:59:59'
      AND (
        `user_trackings`.`utm_source` = 'google_search'
        OR `user_trackings`.`utm_source` = 'google_dsa'
        OR `user_trackings`.`utm_source` = 'google_pmax'
      )
    GROUP BY
      `user_trackings`.`utm_campaign`
    """
    
    query_payload = {
        "database": db_id,
        "type": "native",
        "native": {"query": sql_7d}
    }
    res = requests.post(f"{METABASE_URL}api/dataset", json=query_payload, headers=headers, verify=False)
    rows = res.json().get("data", {}).get("rows", [])
    
    metabase_7d = {}
    for r in rows:
        camp_id = str(r[0])
        cnt = int(r[1])
        metabase_7d[camp_id] = cnt
        
    # Yesterday 2026-08-10
    sql_yd = """
    SELECT
      `user_trackings`.`utm_campaign` AS `utm_campaign`,
      COUNT(*) AS `count`
    FROM
      `user_trackings`
    WHERE
      `user_trackings`.`created_at` >= '2026-08-10 00:00:00'
      AND `user_trackings`.`created_at` <= '2026-08-10 23:59:59'
      AND (
        `user_trackings`.`utm_source` = 'google_search'
        OR `user_trackings`.`utm_source` = 'google_dsa'
        OR `user_trackings`.`utm_source` = 'google_pmax'
      )
    GROUP BY
      `user_trackings`.`utm_campaign`
    """
    res_yd = requests.post(f"{METABASE_URL}api/dataset", json={"database": db_id, "type": "native", "native": {"query": sql_yd}}, headers=headers, verify=False)
    metabase_yd = {}
    for r in res_yd.json().get("data", {}).get("rows", []):
        metabase_yd[str(r[0])] = int(r[1])

    return metabase_7d, metabase_yd

def get_google_ads_data():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    
    # 7-day query
    q_7d = """
        SELECT
            campaign.id,
            campaign.name,
            metrics.cost_micros,
            metrics.clicks
        FROM campaign
        WHERE segments.date BETWEEN '2026-08-03' AND '2026-08-09'
    """
    gads_7d = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_7d):
        for row in batch.results:
            cid = str(row.campaign.id)
            cname = row.campaign.name
            cost = row.metrics.cost_micros / 1000000.0
            if cid not in gads_7d: gads_7d[cid] = {'name': cname, 'cost': 0.0, 'clicks': 0}
            gads_7d[cid]['cost'] += cost
            gads_7d[cid]['clicks'] += row.metrics.clicks
            
    # Yesterday query (2026-08-10)
    q_yd = """
        SELECT
            campaign.id,
            campaign.name,
            metrics.cost_micros,
            metrics.clicks
        FROM campaign
        WHERE segments.date = '2026-08-10'
    """
    gads_yd = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_yd):
        for row in batch.results:
            cid = str(row.campaign.id)
            cname = row.campaign.name
            cost = row.metrics.cost_micros / 1000000.0
            if cid not in gads_yd: gads_yd[cid] = {'name': cname, 'cost': 0.0, 'clicks': 0}
            gads_yd[cid]['cost'] += cost
            gads_yd[cid]['clicks'] += row.metrics.clicks

    return gads_7d, gads_yd

def main():
    print(">>> Fetching Metabase real registrations...")
    meta_7d, meta_yd = get_metabase_7d()
    print(">>> Fetching Google Ads spend...")
    gads_7d, gads_yd = get_google_ads_data()
    
    # Merge and calculate real registration unit price
    all_cids = set(gads_7d.keys()).union(set(gads_yd.keys()))
    
    report_rows = []
    for cid in all_cids:
        name = gads_7d.get(cid, {}).get('name') or gads_yd.get(cid, {}).get('name') or f"Campaign-{cid}"
        
        # 7-day data
        cost_7d = gads_7d.get(cid, {}).get('cost', 0.0)
        regs_7d = meta_7d.get(cid, 0)
        cpr_7d = cost_7d / regs_7d if regs_7d > 0 else (cost_7d if cost_7d > 0 else 0.0)
        
        # Yesterday data
        cost_yd = gads_yd.get(cid, {}).get('cost', 0.0)
        regs_yd = meta_yd.get(cid, 0)
        cpr_yd = cost_yd / regs_yd if regs_yd > 0 else (cost_yd if cost_yd > 0 else 0.0)
        
        report_rows.append({
            'cid': cid, 'name': name,
            'cost_7d': cost_7d, 'regs_7d': regs_7d, 'cpr_7d': cpr_7d,
            'cost_yd': cost_yd, 'regs_yd': regs_yd, 'cpr_yd': cpr_yd
        })
        
    report_rows.sort(key=lambda x: x['regs_7d'], reverse=True)
    
    print("\n" + "="*125)
    print(f"{'Campaign Name':<38} | {'ID':<12} | {'7D Cost':<9} | {'7D Regs':<8} | {'7D Real CPR':<12} | {'YD Cost':<9} | {'YD Regs':<8} | {'YD Real CPR'}")
    print("="*125)
    for r in report_rows:
        if r['cost_7d'] > 0 or r['regs_7d'] > 0 or r['cost_yd'] > 0:
            cpr_7d_str = f"${r['cpr_7d']:.2f}" if r['regs_7d'] > 0 else ("N/A (0)" if r['cost_7d'] > 0 else "$0.00")
            cpr_yd_str = f"${r['cpr_yd']:.2f}" if r['regs_yd'] > 0 else ("N/A (0)" if r['cost_yd'] > 0 else "$0.00")
            print(f"{r['name']:<38} | {r['cid']:<12} | ${r['cost_7d']:<8.2f} | {r['regs_7d']:<8} | {cpr_7d_str:<12} | ${r['cost_yd']:<8.2f} | {r['regs_yd']:<8} | {cpr_yd_str}")

if __name__ == '__main__':
    main()
