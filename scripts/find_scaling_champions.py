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

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    # 1. Metabase 7-day registrations (Aug 5 to Aug 11)
    session_res = requests.post(f"{METABASE_URL}api/session", json={"username": METABASE_USERNAME, "password": METABASE_PASSWORD}, verify=False)
    headers = {"X-Metabase-Session": session_res.json().get("id")}

    sql = """
    SELECT
      `user_trackings`.`utm_campaign` AS `utm_campaign`,
      COUNT(*) AS `count`
    FROM
      `user_trackings`
    WHERE
      `user_trackings`.`created_at` >= '2026-08-05'
      AND `user_trackings`.`created_at` < '2026-08-12'
      AND (
        `user_trackings`.`utm_source` = 'google_search'
        OR `user_trackings`.`utm_source` = 'google_dsa'
        OR `user_trackings`.`utm_source` = 'google_pmax'
      )
    GROUP BY
      `user_trackings`.`utm_campaign`
    """
    res = requests.post(f"{METABASE_URL}api/dataset", headers=headers, json={"database": 2, "type": "native", "native": {"query": sql}}, verify=False)
    mb_data = {str(r[0]): r[1] for r in res.json().get("data", {}).get("rows", [])}

    # 2. Google Ads 7-day spend and Lost IS
    q_ads = """
        SELECT
            campaign.id,
            campaign.name,
            campaign_budget.amount_micros,
            metrics.cost_micros,
            metrics.search_impression_share,
            metrics.search_budget_lost_impression_share
        FROM campaign
        WHERE campaign.status = 'ENABLED'
          AND segments.date >= '2026-08-05'
          AND segments.date <= '2026-08-11'
        ORDER BY metrics.cost_micros DESC
    """
    
    print("=========================================================================================================================")
    print(f"{'Campaign Name':<38} | {'7d Spend':<9} | {'DB Regs':<8} | {'Real CPR':<9} | {'Lost IS(Budget)':<16} | {'Scaling Potential'}")
    print("=========================================================================================================================")
    
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ads):
        for row in batch.results:
            cid = str(row.campaign.id)
            cname = row.campaign.name
            cost = row.metrics.cost_micros / 1000000.0
            lost_b = row.metrics.search_budget_lost_impression_share
            lost_b_str = f"{lost_b*100:.1f}%" if lost_b else "0.0%"
            
            regs = mb_data.get(cid, 0)
            cpr = cost / regs if regs > 0 else float('inf')
            cpr_str = f"${cpr:.2f}" if regs > 0 else "N/A"
            
            potential = "Normal"
            if cpr < 3.50 and regs >= 10:
                if lost_b and lost_b > 0.30:
                    potential = "🔥 HIGH SCALING POTENTIAL (Lost IS > 30%)"
                else:
                    potential = "⭐ Efficient Performer"
            elif cpr > 10.0:
                potential = "🛑 Needs Cut"
                
            print(f"{cname:<38} | ${cost:<8.2f} | {regs:<8} | {cpr_str:<9} | {lost_b_str:<16} | {potential}")

if __name__ == '__main__':
    main()
