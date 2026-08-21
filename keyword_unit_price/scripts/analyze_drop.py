import os
import re

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

r12 = parse_report_file("keyword_unit_price/archive/report_2026-08-12.md")
r18 = parse_report_file("keyword_unit_price/archive/report_2026-08-18.md")
r19 = parse_report_file("keyword_unit_price/archive/report_2026-08-19.md")

print("=== 8.18 vs 8.19 Campaign Diff (Where did the 67 registrations drop?) ===")
diffs = []
for name, d18 in r18.items():
    d19 = r19.get(name, {"cost": 0, "regs": 0, "cpa": 0})
    reg_diff = d19["regs"] - d18["regs"]
    cost_diff = d19["cost"] - d18["cost"]
    diffs.append((name, reg_diff, cost_diff, d18["regs"], d19["regs"], d18["cost"], d19["cost"]))

diffs.sort(key=lambda x: x[1]) # sort by biggest registration drop

print(f"{'Campaign Name':<45} | {'Reg Diff':<8} | {'Cost Diff':<10} | {'8.18 Reg':<8} | {'8.19 Reg':<8} | {'8.18 Cost':<10} | {'8.19 Cost':<10}")
print("-" * 115)
for item in diffs[:15]: # Top 15 drops
    print(f"{item[0]:<45} | {item[1]:<8} | ${item[2]:<9.2f} | {item[3]:<8} | {item[4]:<8} | ${item[5]:<9.2f} | ${item[6]:<9.2f}")

print("\n=== Top Gainers ===")
for item in diffs[-5:]:
    print(f"{item[0]:<45} | {item[1]:<8} | ${item[2]:<9.2f} | {item[3]:<8} | {item[4]:<8} | ${item[5]:<9.2f} | ${item[6]:<9.2f}")

print("\n=== 8.12 vs 8.19 (Week over Week Wednesday) Diff ===")
diffs_wow = []
for name, d12 in r12.items():
    d19 = r19.get(name, {"cost": 0, "regs": 0, "cpa": 0})
    reg_diff = d19["regs"] - d12["regs"]
    cost_diff = d19["cost"] - d12["cost"]
    diffs_wow.append((name, reg_diff, cost_diff, d12["regs"], d19["regs"], d12["cost"], d19["cost"]))

diffs_wow.sort(key=lambda x: x[1])
print(f"{'Campaign Name':<45} | {'Reg Diff':<8} | {'Cost Diff':<10} | {'8.12 Reg':<8} | {'8.19 Reg':<8} | {'8.12 Cost':<10} | {'8.19 Cost':<10}")
print("-" * 115)
for item in diffs_wow[:15]:
    print(f"{item[0]:<45} | {item[1]:<8} | ${item[2]:<9.2f} | {item[3]:<8} | {item[4]:<8} | ${item[5]:<9.2f} | ${item[6]:<9.2f}")
