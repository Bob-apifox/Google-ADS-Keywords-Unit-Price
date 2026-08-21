import os

def parse_report_file(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    campaigns = {}
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
                    campaigns[name] = {"id": c_id, "cost": cost, "regs": regs, "cpa": cpa}
                except ValueError:
                    continue
    return campaigns

r19 = parse_report_file("keyword_unit_price/archive/report_2026-08-19.md")
r20 = parse_report_file("keyword_unit_price/archive/report_2026-08-20.md")

print("=== 8.19 vs 8.20 Campaign Diff (Where did gains and losses come from?) ===")
diffs = []
for name, d20 in r20.items():
    d19 = r19.get(name, {"cost": 0, "regs": 0, "cpa": 999999})
    reg_diff = d20["regs"] - d19["regs"]
    cost_diff = d20["cost"] - d19["cost"]
    diffs.append((name, reg_diff, cost_diff, d19["regs"], d20["regs"], d19["cost"], d20["cost"], d20["cpa"]))

# Sort by reg diff descending
diffs.sort(key=lambda x: x[1], reverse=True)

print(f"{'Campaign Name':<42} | {'Reg Diff':<8} | {'Cost Diff':<10} | {'8.19 Reg':<8} | {'8.20 Reg':<8} | {'8.20 Cost':<10} | {'8.20 CPA':<8}")
print("-" * 105)
print("--- TOP GAINERS (增量支撑) ---")
for item in diffs[:10]:
    cpa_str = f"${item[7]:.2f}" if item[7] < 999999 else "N/A"
    print(f"{item[0]:<42} | +{item[1]:<7} | ${item[2]:<9.2f} | {item[3]:<8} | {item[4]:<8} | ${item[6]:<9.2f} | {cpa_str:<8}")

print("\n--- TOP DROPS (主要拖累) ---")
for item in diffs[-10:]:
    cpa_str = f"${item[7]:.2f}" if item[7] < 999999 else "N/A"
    print(f"{item[0]:<42} | {item[1]:<8} | ${item[2]:<9.2f} | {item[3]:<8} | {item[4]:<8} | ${item[6]:<9.2f} | {cpa_str:<8}")
