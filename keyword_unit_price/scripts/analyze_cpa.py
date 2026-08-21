import os
import sys
import re
import datetime
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

def parse_report():
    report_path = os.path.join(os.path.dirname(__file__), "../reports/final_registration_report.md")
    # If not found, try archive
    if not os.path.exists(report_path):
        today = datetime.date.today()
        # Look for the last few days in archive just in case
        for i in range(5):
            date_str = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            archive_path = os.path.join(os.path.dirname(__file__), f"../archive/report_{date_str}.md")
            if os.path.exists(archive_path):
                report_path = archive_path
                break
                
    if not os.path.exists(report_path):
        print("Could not find any recent report to parse.")
        return None, "0.00", []
        
    print(f"Reading campaigns from: {report_path}")
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    date_match = re.search(r"> \*\*报告日期\*\*: `(.*?)`", content)
    report_date = date_match.group(1) if date_match else "Unknown"
    
    avg_cpa_match = re.search(r"\*\*平均注册单价 \(Avg\. CPA\)\*\* \| `\$(.*?)`", content)
    avg_cpa = avg_cpa_match.group(1) if avg_cpa_match else "0.00"
    
    campaigns = []
    # Match table rows: | 1 | `ID` | Name | Cost | Regs | CPA | Status |
    for line in content.split("\n"):
        if line.startswith("|") and "`" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 8:
                try:
                    c_id = parts[2].replace("`", "")
                    name = parts[3]
                    cost = float(parts[4].replace("$", "").replace(",", ""))
                    regs = int(parts[5].replace(",", ""))
                    cpa_str = parts[6].replace("**", "").replace("$", "")
                    
                    if cpa_str == "N/A":
                        cpa = float('inf')
                    else:
                        cpa = float(cpa_str)
                        
                    if cpa > 4.0 or cpa == float('inf'):
                        campaigns.append({
                            "id": c_id,
                            "name": name,
                            "cost": cost,
                            "regs": regs,
                            "cpa": cpa_str
                        })
                except ValueError:
                    continue
                    
    return report_date, avg_cpa, campaigns

def get_ad_groups(client, campaign_id):
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            ad_group.name,
            metrics.cost_micros,
            metrics.conversions,
            metrics.clicks
        FROM ad_group
        WHERE segments.date DURING LAST_7_DAYS
          AND campaign.id = {campaign_id}
        ORDER BY metrics.cost_micros DESC
        LIMIT 5
    """
    results = []
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                cost = row.metrics.cost_micros / 1000000.0
                clicks = row.metrics.clicks
                conversions = row.metrics.conversions
                cpa = cost / conversions if conversions > 0 else 0
                results.append({
                    "name": row.ad_group.name,
                    "cost": cost,
                    "conversions": conversions,
                    "cpa": cpa,
                    "clicks": clicks
                })
    except Exception as e:
        print(f"Error fetching ad groups: {e}")
    return results

def get_keywords(client, campaign_id):
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.quality_info.quality_score,
            metrics.cost_micros,
            metrics.conversions,
            metrics.clicks
        FROM keyword_view
        WHERE segments.date DURING LAST_7_DAYS
          AND campaign.id = {campaign_id}
        ORDER BY metrics.cost_micros DESC
        LIMIT 10
    """
    results = []
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                results.append({
                    "text": row.ad_group_criterion.keyword.text,
                    "qs": row.ad_group_criterion.quality_info.quality_score if row.ad_group_criterion.quality_info.quality_score else "N/A",
                    "cost": row.metrics.cost_micros / 1000000.0,
                    "conversions": row.metrics.conversions,
                    "clicks": row.metrics.clicks
                })
    except Exception as e:
        pass
    return results

def get_search_terms(client, campaign_id):
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            search_term_view.search_term,
            metrics.cost_micros,
            metrics.clicks
        FROM search_term_view
        WHERE segments.date DURING LAST_7_DAYS
          AND campaign.id = {campaign_id}
          AND metrics.conversions = 0
          AND metrics.cost_micros > 1000000
        ORDER BY metrics.cost_micros DESC
        LIMIT 10
    """
    results = []
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                results.append({
                    "term": row.search_term_view.search_term,
                    "cost": row.metrics.cost_micros / 1000000.0,
                    "clicks": row.metrics.clicks
                })
    except Exception as e:
        pass
    return results

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    report_date, avg_cpa, campaigns = parse_report()
    if not campaigns:
        print("No campaigns with CPA > $4.0 found or report missing.")
        return

    print(f"=== Generating Optimization Plan for {report_date} ===")
    
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    except Exception as e:
        print(f"Failed to load Google Ads client: {e}")
        return

    md = f"# 🎯 Google Ads 广告优化建议方案\n> **分析日期**: `{report_date}` | **平均 CPA 基准**: `${avg_cpa}`\n\n"
    md += "本报告针对昨日表现不佳（高 CPA 或高消耗无转化）的广告系列进行了深度挖掘，并提供了优化建议。\n\n---\n"
    
    for camp in campaigns:
        print(f"Analyzing campaign: {camp['name']} ({camp['id']})")
        md += f"## 🚩 重点优化对象: {camp['name']} (`{camp['id']}`)\n"
        md += f"> **昨日数据**: 消耗 `${camp['cost']:.2f}` | 注册 `{camp['regs']}` | CPA `${camp['cpa']}`\n\n"
        
        ad_groups = get_ad_groups(client, camp['id'])
        md += "### 📦 广告组表现 (Top Ad Groups by Cost - Last 7 Days)\n"
        md += "| 广告组 | 消耗 (USD) | 转化 | CPA | 点击数 | 建议 |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        if ad_groups:
            for ag in ad_groups:
                if ag['conversions'] == 0:
                    advice = "📝 无转化，需优化广告文案或暂停"
                elif ag['cpa'] > 4.0:
                    advice = "⚠️ CPA过高，建议降低出价或排查词"
                else:
                    advice = "✅ 表现正常"
                md += f"| {ag['name']} | ${ag['cost']:.2f} | {ag['conversions']} | ${ag['cpa']:.2f} | {ag['clicks']} | {advice} |\n"
        else:
            md += "_暂无数据_\n"
        md += "\n"
        
        keywords = get_keywords(client, camp['id'])
        md += "### 🔑 关键词分析 (Top Keywords by Cost - Last 7 Days)\n"
        md += "| 关键词 | 质量得分 | 消耗 (USD) | 转化 | 点击 | 状态 |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        if keywords:
            for kw in keywords:
                status = "正常"
                if kw['qs'] != "N/A" and kw['qs'] < 5:
                    status = "📉 质量分低 (相关性差)"
                md += f"| `{kw['text']}` | {kw['qs']} | ${kw['cost']:.2f} | {kw['conversions']} | {kw['clicks']} | {status} |\n"
        else:
            md += "_该广告系列无关键词层级数据（可能是 PMax 或 DSA 广告系列）。_\n"
        md += "\n"
        
        search_terms = get_search_terms(client, camp['id'])
        md += "### 🔍 潜在浪费搜索词 (High Cost, Zero Conversions - Last 7 Days)\n"
        md += "| 搜索词 | 消耗 (USD) | 点击数 | 处理建议 |\n| :--- | :--- | :--- | :--- |\n"
        if search_terms:
            for st in search_terms:
                md += f"| `{st['term']}` | ${st['cost']:.2f} | {st['clicks']} | 建议添加为否定词 |\n"
        else:
            md += "_暂无明显的浪费搜索词_\n"
        
        md += "\n---\n"
        
    md += "\n*报告由分析脚本自动生成，建议结合具体业务场景手动调整。*\n"
    
    out_dir = os.path.join(os.path.dirname(__file__), "../reports")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"optimization_plan_{report_date}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
        
    print(f"\n✅ 优化建议已生成至: {out_path}")

if __name__ == "__main__":
    main()
