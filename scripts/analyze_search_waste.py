import json

def main():
    with open("keyword_unit_price/reports/search_campaigns_waste_audit.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    severe_waste = []
    moderate_waste = []
    healthy = []
    zero_spend = []

    for c in data:
        cost_14d = c["cost_14d"]
        reg_14d = c["reg_14d"]
        cpr_14d = c["cpr_14d"]
        cost_7d = c["cost_7d"]
        reg_7d = c["reg_7d"]
        cpr_7d = c["cpr_7d"]
        cost_30d = c["cost_30d"]
        reg_30d = c["reg_30d"]
        status = c["status"]

        if cost_14d < 1.0 and cost_30d < 1.0:
            zero_spend.append(c)
            continue

        if reg_14d == 0 and cost_14d > 20.0:
            severe_waste.append(c)
        elif cpr_14d >= 8.0:
            severe_waste.append(c)
        elif 5.0 <= cpr_14d < 8.0:
            moderate_waste.append(c)
        else:
            healthy.append(c)

    print("==================================================================================================")
    print("[1. SEVERE LONG-TERM WASTE: 14D 0 Regs OR CPR > $8.00]")
    print("==================================================================================================")
    for c in severe_waste:
        cpr14_s = f"${c['cpr_14d']:.2f}" if c['cpr_14d'] < 999 else "0 Regs"
        cpr7_s = f"${c['cpr_7d']:.2f}" if c['cpr_7d'] < 999 else "0 Regs"
        print(f"[{c['name']:<38}] ID: {c['cid']} | 14D Spend: ${c['cost_14d']:<7.2f} | 14D Regs: {c['reg_14d']:<3} ({cpr14_s:<7}) | 7D Spend: ${c['cost_7d']:<6.2f} | 7D Regs: {c['reg_7d']:<2} ({cpr7_s})")

    print("\n==================================================================================================")
    print("[2. MODERATE WASTE / WARNING: 14D CPR $5.00 ~ $8.00]")
    print("==================================================================================================")
    for c in moderate_waste:
        print(f"[{c['name']:<38}] ID: {c['cid']} | 14D Spend: ${c['cost_14d']:<7.2f} | 14D Regs: {c['reg_14d']:<3} (${c['cpr_14d']:.2f}) | 7D Spend: ${c['cost_7d']:<6.2f} | 7D Regs: {c['reg_7d']:<2} (${c['cpr_7d']:.2f})")

    print("\n==================================================================================================")
    print("[3. HEALTHY TOP PERFORMERS: 14D CPR < $5.00]")
    print("==================================================================================================")
    for c in healthy:
        print(f"[{c['name']:<38}] ID: {c['cid']} | 14D Spend: ${c['cost_14d']:<7.2f} | 14D Regs: {c['reg_14d']:<3} (${c['cpr_14d']:.2f}) | 7D Spend: ${c['cost_7d']:<6.2f} | 7D Regs: {c['reg_7d']:<2} (${c['cpr_7d']:.2f})")

    print(f"\n[4. ZERO SPEND / SLEEPING CAMPAIGNS]: Total {len(zero_spend)} campaigns")

if __name__ == '__main__':
    main()
