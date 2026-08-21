import os
import sys
import json
import datetime
import requests
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 1. Configuration & Proxy
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

METABASE_URL = "https://metabase.apifox.cn/"
METABASE_USERNAME = "bob@apifox.com"
METABASE_PASSWORD = "08103245981Zgh"
GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

def get_metabase_data():
    print(">>> Logging into Metabase...")
    session_res = requests.post(f"{METABASE_URL}api/session", json={
        "username": METABASE_USERNAME, 
        "password": METABASE_PASSWORD
    }, verify=False)
    session_id = session_res.json().get("id")
    if not session_id:
        print(f"FAILED to login to Metabase: {session_res.text}")
        return {}

    headers = {"X-Metabase-Session": session_id}
    sql = """
    SELECT
      `user_trackings`.`utm_campaign` AS `utm_campaign`,
      COUNT(*) AS `count`
    FROM
      `user_trackings`
    WHERE
      `user_trackings`.`created_at` >= DATE(DATE_ADD(NOW(6), INTERVAL -1 day))
      AND `user_trackings`.`created_at` < DATE(NOW(6))
      AND (
        `user_trackings`.`utm_source` = 'google_search'
        OR `user_trackings`.`utm_source` = 'google_dsa'
        OR `user_trackings`.`utm_source` = 'google_pmax'
      )
    GROUP BY
      `user_trackings`.`utm_campaign`
    """
    
    print(">>> Fetching data from Metabase...")
    db_res = requests.get(f"{METABASE_URL}api/database", headers=headers, verify=False)
    try:
        db_data = db_res.json()
    except Exception as e:
        print(f"FAILED to parse Metabase database response as JSON: {e}")
        return {}

    databases = db_data.get('data') if isinstance(db_data, dict) else db_data
    if not databases or not isinstance(databases, list):
        print(f"FAILED: Metabase database list is empty. Response: {db_data}")
        return {}
    
    db_id = None
    for db in databases:
        if db.get('name') == 'Apidog RDS':
            db_id = db['id']
            print(f">>> Found Metabase database: Apidog RDS (ID: {db_id})")
            break
    
    if db_id is None:
        db_id = databases[0]['id']
    
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
            campaign = row[0]
            count = row[1]
            results[campaign] = count
    return results

def get_google_ads_data():
    print(">>> Fetching Google Ads cost data...")
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    
    query = """
        SELECT
            campaign.id,
            campaign.name,
            metrics.cost_micros
        FROM campaign
        WHERE segments.date DURING YESTERDAY
    """
    
    id_to_name = {}
    id_to_cost = {}
    name_to_id = {}
    
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                campaign_name = row.campaign.name
                campaign_id = str(row.campaign.id)
                cost = row.metrics.cost_micros / 1000000.0
                
                id_to_name[campaign_id] = campaign_name
                id_to_cost[campaign_id] = cost
                name_to_id[campaign_name] = campaign_id
                
    except GoogleAdsException as ex:
        print(f"Google Ads API Error: {ex}")
    return id_to_name, id_to_cost, name_to_id

def get_top_keywords(client):
    print(">>> Fetching TOP 20 Keywords (Last 7 Days)...")
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
            campaign.name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            metrics.clicks,
            metrics.cost_micros
        FROM keyword_view
        WHERE segments.date DURING LAST_7_DAYS
          AND metrics.clicks > 20
        ORDER BY metrics.clicks DESC
        LIMIT 20
    """
    keywords = []
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                cost = row.metrics.cost_micros / 1000000.0
                clicks = row.metrics.clicks
                keywords.append({
                    "campaign": row.campaign.name,
                    "keyword": row.ad_group_criterion.keyword.text,
                    "match_type": row.ad_group_criterion.keyword.match_type.name,
                    "clicks": clicks,
                    "cost": cost,
                    "cpc": cost / clicks if clicks > 0 else 0
                })
    except Exception as e:
        print(f"Error fetching top keywords: {e}")
    return keywords

def get_postman_keywords(client):
    print(">>> Fetching POSTMAN Keywords (Last 14 Days)...")
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
            campaign.name,
            ad_group_criterion.keyword.text,
            metrics.clicks,
            metrics.cost_micros
        FROM keyword_view
        WHERE segments.date DURING LAST_14_DAYS
          AND campaign.name LIKE '%Postman%'
          AND metrics.clicks > 10
        ORDER BY metrics.clicks DESC
        LIMIT 20
    """
    keywords = []
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                cost = row.metrics.cost_micros / 1000000.0
                clicks = row.metrics.clicks
                keywords.append({
                    "campaign": row.campaign.name,
                    "keyword": row.ad_group_criterion.keyword.text,
                    "clicks": clicks,
                    "cost": cost,
                    "cpc": cost / clicks if clicks > 0 else 0
                })
    except Exception as e:
        print(f"Error fetching Postman keywords: {e}")
    return keywords

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"=== Generating Integrated Report for {yesterday} ===")
    
    metabase_counts = get_metabase_data()
    
    # 1. Google Ads Data
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    id_to_name, id_to_cost, name_to_id = get_google_ads_data()
    
    top_keywords = get_top_keywords(client)
    postman_keywords = get_postman_keywords(client)
    
    report_map = {}
    total_cost = 0
    total_regs = 0
    
    for campaign_id, cost in id_to_cost.items():
        if cost > 0:
            total_cost += cost
            report_map[campaign_id] = {
                "ID": campaign_id, 
                "Name": id_to_name.get(campaign_id, "Unknown"), 
                "Cost": cost, 
                "Registrations": 0
            }

    for identifier, count in metabase_counts.items():
        campaign_id = identifier if identifier in id_to_name else name_to_id.get(identifier)
        if campaign_id:
            if campaign_id not in report_map:
                report_map[campaign_id] = {
                    "ID": campaign_id, 
                    "Name": id_to_name.get(campaign_id, identifier), 
                    "Cost": id_to_cost.get(campaign_id, 0.0), 
                    "Registrations": 0
                }
            report_map[campaign_id]["Registrations"] += count
            total_regs += count

    report_data = list(report_map.values())
    for item in report_data:
        count = item["Registrations"]
        cost = item["Cost"]
        item["Unit Price"] = cost / count if count > 0 else (999999 if cost > 0 else 0)

    report_data.sort(key=lambda x: x['Unit Price'], reverse=True)
    avg_unit_price = total_cost / total_regs if total_regs > 0 else 0

    md = f"""# 📊 Google Ads 综合分析报告 (Integrated Report)
> **报告日期**: `{yesterday}` | **生成时间**: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

---

## 📈 数据概览 (Summary)
| 指标 | 数值 |
| :--- | :--- |
| **总消耗 (Total Cost)** | `${total_cost:,.2f}` |
| **总注册数 (Total Registrations)** | `{total_regs:,}` |
| **平均注册单价 (Avg. CPA)** | `${avg_unit_price:,.2f}` |

---

## 🚀 注册单价明细 (Campaign CPA Breakdown)
*昨日数据按单价排名 (从高到低)*

| 排名 | Campaign ID | 广告系列名称 | 消耗 (USD) | 注册数 | 注册单价 | 状态 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    
    for i, item in enumerate(report_data, 1):
        cost_str = f"${item['Cost']:,.2f}"
        reg_str = f"{item['Registrations']:,}"
        
        if item['Unit Price'] >= 999999:
            up_str = "N/A"
            status = "🔴 无转化 (High Risk)"
        else:
            up_str = f"${item['Unit Price']:,.2f}"
            if item['Unit Price'] > avg_unit_price * 1.5:
                status = "⚠️ 成本偏高"
            elif item['Unit Price'] < avg_unit_price * 0.5:
                status = "✅ 表现优异"
            else:
                status = "正常"

        md += f"| {i} | `{item['ID']}` | {item['Name']} | {cost_str} | {reg_str} | **{up_str}** | {status} |\n"

    md += "\n---\n\n## 🔍 关键词洞察 (Keyword Insights)\n"
    
    md += "\n### 🥇 TOP 20 高频词 (近 7 天)\n"
    md += "| 排名 | 关键词 | 匹配类型 | 广告系列 | 点击数 | 消耗 (USD) | 点击单价 (CPC) |\n"
    md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for i, kw in enumerate(top_keywords, 1):
        md += f"| {i} | `{kw['keyword']}` | {kw['match_type']} | {kw['campaign']} | {kw['clicks']} | ${kw['cost']:.2f} | **${kw['cpc']:.2f}** |\n"

    md += "\n### 🛡️ Postman 竞品词专题 (近 14 天)\n"
    md += "| 排名 | 关键词 | 广告系列 | 点击数 | 消耗 (USD) | 点击单价 (CPC) |\n"
    md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for i, kw in enumerate(postman_keywords, 1):
        md += f"| {i} | `{kw['keyword']}` | {kw['campaign']} | {kw['clicks']} | ${kw['cost']:.2f} | **${kw['cpc']:.2f}** |\n"

    md += "\n---\n*报告由自动化脚本生成。如有疑问请检查 Google Ads 后台与 Metabase `Apidog RDS` 库。*"

    reports_dir = os.path.join(os.path.dirname(__file__), "../reports")
    archive_dir = os.path.join(os.path.dirname(__file__), "../archive")
    
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)
    
    output_path = os.path.join(reports_dir, "final_registration_report.md")
    archive_path = os.path.join(archive_dir, f"report_{yesterday}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)
    
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"\n✅ 报告已成功生成并保存至: {output_path}")
    print(f"📦 历史存档已保存至: {archive_path}")

if __name__ == "__main__":
    main()
