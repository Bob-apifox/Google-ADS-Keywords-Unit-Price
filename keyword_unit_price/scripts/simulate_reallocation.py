import os
import sys
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

def parse_report(filepath):
    if not os.path.exists(filepath): return {}
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    camps = {}
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
                    cpa = float(cpa_str) if cpa_str != "N/A" else 999999
                    camps[name] = {"id": c_id, "cost": cost, "regs": regs, "cpa": cpa}
                except ValueError:
                    continue
    return camps

r18 = parse_report("keyword_unit_price/archive/report_2026-08-18.md")
r19 = parse_report("keyword_unit_price/archive/report_2026-08-19.md")

# Fetch current live budgets from Google Ads API
client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
ga_service = client.get_service("GoogleAdsService")
query = """
    SELECT
        campaign.id,
        campaign.name,
        campaign_budget.amount_micros,
        campaign.maximize_conversions.target_cpa_micros,
        campaign.target_cpa.target_cpa_micros,
        campaign.bidding_strategy_type
    FROM campaign
    WHERE campaign.status = 'ENABLED'
"""
stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
live_data = {}
for batch in stream:
    for row in batch.results:
        c = row.campaign
        b = row.campaign_budget
        tcpa = (c.maximize_conversions.target_cpa_micros or c.target_cpa.target_cpa_micros or 0) / 1e6
        live_data[c.name] = {
            "id": str(c.id),
            "budget": b.amount_micros / 1e6 if b.amount_micros else 0,
            "tcpa": tcpa,
            "bidding_type": c.bidding_strategy_type.name
        }

print("=== Campaign Performance & Current Budget Matrix ===")
rows = []
for name, live in live_data.items():
    d18 = r18.get(name, {"cost": 0, "regs": 0, "cpa": 999999})
    d19 = r19.get(name, {"cost": 0, "regs": 0, "cpa": 999999})
    
    total_cost_2d = d18["cost"] + d19["cost"]
    total_regs_2d = d18["regs"] + d19["regs"]
    cpa_2d = total_cost_2d / total_regs_2d if total_regs_2d > 0 else (999999 if total_cost_2d > 0 else 0)
    
    rows.append({
        "name": name,
        "id": live["id"],
        "budget": live["budget"],
        "tcpa": live["tcpa"],
        "cost_2d": total_cost_2d,
        "regs_2d": total_regs_2d,
        "cpa_2d": cpa_2d
    })

# Sort by CPA 2d
rows.sort(key=lambda x: x["cpa_2d"])

print(f"{'Campaign Name':<42} | {'Budget':<8} | {'2D Cost':<9} | {'2D Regs':<8} | {'2D CPA':<8} | Tier")
print("-" * 95)
for r in rows:
    cpa_str = f"${r['cpa_2d']:.2f}" if r['cpa_2d'] < 999999 else "N/A"
    if r['regs_2d'] >= 10 and r['cpa_2d'] <= 3.5:
        tier = "🚀 Tier 1 (Golden Engine - Scale)"
    elif r['regs_2d'] >= 5 and r['cpa_2d'] <= 4.0:
        tier = "✨ Tier 2 (Steady Producer)"
    elif r['cpa_2d'] > 6.0 or r['regs_2d'] == 0:
        tier = "✂️ Tier 3 (Bleeder - Cut Budget)"
    else:
        tier = "⚖️ Tier 4 (Neutral)"
    print(f"{r['name']:<42} | ${r['budget']:<7.1f} | ${r['cost_2d']:<8.2f} | {r['regs_2d']:<8} | {cpa_str:<8} | {tier}")
