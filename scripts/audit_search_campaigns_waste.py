import os
import requests
import json
from google.ads.googleads.client import GoogleAdsClient
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

METABASE_URL = "https://metabase.apifox.cn/"
METABASE_USERNAME = "bob@apifox.com"
METABASE_PASSWORD = "08103245981Zgh"

def get_metabase_data_days(days):
    session_res = requests.post(f"{METABASE_URL}api/session", json={
        "username": METABASE_USERNAME, 
        "password": METABASE_PASSWORD
    }, verify=False)
    headers = {"X-Metabase-Session": session_res.json().get("id")}

    db_res = requests.get(f"{METABASE_URL}api/database", headers=headers, verify=False)
    databases = db_res.json().get('data') if isinstance(db_res.json(), dict) else db_res.json()
    db_id = None
    for db in databases:
        if db.get('name') == 'Apidog RDS':
            db_id = db['id']
            break
    if db_id is None:
        db_id = 3

    sql = f"""
    SELECT
      `user_trackings`.`utm_campaign` AS `utm_campaign`,
      COUNT(*) AS `count`
    FROM
      `user_trackings`
    WHERE
      `user_trackings`.`created_at` >= DATE(DATE_ADD(NOW(6), INTERVAL -{days} day))
      AND `user_trackings`.`created_at` < DATE(NOW(6))
      AND (
        `user_trackings`.`utm_source` = 'google_search'
        OR `user_trackings`.`utm_source` = 'google_dsa'
      )
    GROUP BY
      `user_trackings`.`utm_campaign`
    """
    query_payload = {
        "database": db_id,
        "type": "native",
        "native": {"query": sql},
        "parameters": []
    }
    res = requests.post(f"{METABASE_URL}api/dataset", json=query_payload, headers=headers, verify=False)
    data = res.json()
    results = {}
    if 'data' in data and 'rows' in data['data']:
        for row in data['data']['rows']:
            campaign = str(row[0]).strip()
            count = int(row[1])
            results[campaign] = count
    return results

def query_google_ads_cost(client, customer_id, days):
    ga_service = client.get_service("GoogleAdsService")
    q = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_budget.amount_micros,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions
        FROM campaign
        WHERE segments.date DURING LAST_{days}_DAYS
          AND campaign.advertising_channel_type = 'SEARCH'
          AND campaign.status != 'REMOVED'
    """
    # Note: Google Ads API has DURING LAST_7_DAYS, LAST_14_DAYS, LAST_30_DAYS
    enum_str = f"LAST_{days}_DAYS" if days in [7, 14, 30] else "LAST_7_DAYS"
    q = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_budget.amount_micros,
            metrics.cost_micros,
            metrics.clicks
        FROM campaign
        WHERE segments.date DURING {enum_str}
          AND campaign.advertising_channel_type = 'SEARCH'
          AND campaign.status != 'REMOVED'
    """
    results = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=q):
        for row in batch.results:
            cid = str(row.campaign.id)
            cname = row.campaign.name
            cstatus = row.campaign.status.name
            cost = row.metrics.cost_micros / 1000000.0
            budget = row.campaign_budget.amount_micros / 1000000.0 if row.campaign_budget.amount_micros else 0.0
            
            if cid not in results:
                results[cid] = {
                    "id": cid,
                    "name": cname,
                    "status": cstatus,
                    "budget": budget,
                    "cost": 0.0
                }
            results[cid]["cost"] += cost
    return results

def main():
    print("=== PULLING METABASE REAL REGS & GOOGLE ADS SPEND FOR SEARCH CAMPAIGNS ===")
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)

    regs_7d = get_metabase_data_days(7)
    regs_14d = get_metabase_data_days(14)
    regs_30d = get_metabase_data_days(30)
    print(f">>> Fetched Metabase data: 7D campaigns={len(regs_7d)}, 14D campaigns={len(regs_14d)}, 30D campaigns={len(regs_30d)}")

    costs_7d = query_google_ads_cost(client, CUSTOMER_ID, 7)
    costs_14d = query_google_ads_cost(client, CUSTOMER_ID, 14)
    costs_30d = query_google_ads_cost(client, CUSTOMER_ID, 30)

    compiled = []
    for cid, data in costs_14d.items():
        name = data["name"]
        status = data["status"]
        budget = data["budget"]

        cost_7 = costs_7d.get(cid, {}).get("cost", 0.0)
        reg_7 = regs_7d.get(cid, 0)
        cpr_7 = (cost_7 / reg_7) if reg_7 > 0 else (9999.0 if cost_7 > 0 else 0.0)

        cost_14 = data["cost"]
        reg_14 = regs_14d.get(cid, 0)
        cpr_14 = (cost_14 / reg_14) if reg_14 > 0 else (9999.0 if cost_14 > 0 else 0.0)

        cost_30 = costs_30d.get(cid, {}).get("cost", 0.0)
        reg_30 = regs_30d.get(cid, 0)
        cpr_30 = (cost_30 / reg_30) if reg_30 > 0 else (9999.0 if cost_30 > 0 else 0.0)

        compiled.append({
            "cid": cid,
            "name": name,
            "status": status,
            "budget": budget,
            "cost_7d": cost_7,
            "reg_7d": reg_7,
            "cpr_7d": cpr_7,
            "cost_14d": cost_14,
            "reg_14d": reg_14,
            "cpr_14d": cpr_14,
            "cost_30d": cost_30,
            "reg_30d": reg_30,
            "cpr_30d": cpr_30
        })

    with open("keyword_unit_price/reports/search_campaigns_waste_audit.json", "w", encoding="utf-8") as f:
        json.dump(compiled, f, indent=2, ensure_ascii=False)

    # Classify
    severe_waste = []
    moderate_waste = []
    healthy = []
    zero_spend = []

    for c in compiled:
        if c["cost_14d"] < 1.0 and c["cost_30d"] < 1.0:
            zero_spend.append(c)
        elif (c["reg_14d"] <= 2 and c["cost_14d"] >= 30.0) or c["cpr_14d"] >= 7.50:
            severe_waste.append(c)
        elif 4.50 <= c["cpr_14d"] < 7.50:
            moderate_waste.append(c)
        else:
            healthy.append(c)

    severe_waste.sort(key=lambda x: (x["cpr_14d"] if x["cpr_14d"] < 999 else 9999, x["cost_14d"]), reverse=True)
    moderate_waste.sort(key=lambda x: x["cpr_14d"], reverse=True)
    healthy.sort(key=lambda x: x["reg_14d"], reverse=True)

    print("\n" + "="*145)
    print("[1. SEVERE LONG-TERM WASTE / 0 REGS OR ULTRA HIGH CPR >= $7.50]")
    print("="*145)
    for c in severe_waste:
        cpr14_s = f"${c['cpr_14d']:.2f}" if c['cpr_14d'] < 999 else "0 Regs"
        cpr7_s = f"${c['cpr_7d']:.2f}" if c['cpr_7d'] < 999 else "0 Regs"
        print(f"[{c['name']:<36}] ID: {c['cid']} | 14D: ${c['cost_14d']:<7.2f} / {c['reg_14d']:<3}人 ({cpr14_s:<8}) | 7D: ${c['cost_7d']:<6.2f} / {c['reg_7d']:<2}人 ({cpr7_s:<7}) | 30D: ${c['cost_30d']:<7.2f} / {c['reg_30d']}人")

    print("\n" + "="*145)
    print("[2. MODERATE COST WARNING / CPR $4.50 ~ $7.50]")
    print("="*145)
    for c in moderate_waste:
        print(f"[{c['name']:<36}] ID: {c['cid']} | 14D: ${c['cost_14d']:<7.2f} / {c['reg_14d']:<3}人 (${c['cpr_14d']:<6.2f}) | 7D: ${c['cost_7d']:<6.2f} / {c['reg_7d']:<2}人 (${c['cpr_7d']:<5.2f}) | 30D: ${c['cost_30d']:<7.2f} / {c['reg_30d']}人")

    print("\n" + "="*145)
    print("[3. HEALTHY PROFITABLE SEARCH ENGINES / CPR < $4.50]")
    print("="*145)
    for c in healthy:
        print(f"[{c['name']:<36}] ID: {c['cid']} | 14D: ${c['cost_14d']:<7.2f} / {c['reg_14d']:<3}人 (${c['cpr_14d']:<6.2f}) | 7D: ${c['cost_7d']:<6.2f} / {c['reg_7d']:<2}人 (${c['cpr_7d']:<5.2f}) | 30D: ${c['cost_30d']:<7.2f} / {c['reg_30d']}人")

if __name__ == '__main__':
    main()
