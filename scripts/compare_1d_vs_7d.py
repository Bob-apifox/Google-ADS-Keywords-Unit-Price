import re

# Let's extract 7-day data from optimization_plan_2026-08-10.md
with open('keyword_unit_price/reports/optimization_plan_2026-08-10.md', 'r', encoding='utf-8') as f:
    content = f.read()

sections = content.split('## 🚩 重点优化对象:')
print(f"Total sections: {len(sections)-1}")

results = []
for sec in sections[1:]:
    camp_match = re.search(r'^(.*?)\s*\(`(.*?)`\)', sec.strip())
    if not camp_match: continue
    camp_name = camp_match.group(1).strip()
    camp_id = camp_match.group(2).strip()
    
    # Yesterday data
    yd_match = re.search(r'> \*\*昨日数据\*\*: 消耗 `\$(.*?)` \| 注册 `(.*?)` \| CPA `\$(.*?)`', sec)
    yd_cost = float(yd_match.group(1)) if yd_match else 0.0
    yd_regs = int(yd_match.group(2)) if yd_match else 0
    yd_cpa = yd_match.group(3) if yd_match else 'N/A'
    
    # 7-day ad groups total
    ag_table = re.search(r'### 📦 广告组表现.*?\n\| :---.*?\n(.*?)\n\n', sec, re.DOTALL)
    tot_7d_cost = 0.0
    tot_7d_conv = 0.0
    if ag_table:
        for row in ag_table.group(1).strip().split('\n'):
            parts = [p.strip() for p in row.split('|')]
            if len(parts) >= 7:
                try:
                    c = float(parts[2].replace('$', '').replace(',', ''))
                    conv = float(parts[3].replace(',', ''))
                    tot_7d_cost += c
                    tot_7d_conv += conv
                except:
                    pass
    
    cpa_7d = tot_7d_cost / tot_7d_conv if tot_7d_conv > 0 else float('inf')
    results.append({
        'name': camp_name, 'id': camp_id,
        'yd_cost': yd_cost, 'yd_regs': yd_regs, 'yd_cpa': yd_cpa,
        '7d_cost': tot_7d_cost, '7d_conv': tot_7d_conv, '7d_cpa': cpa_7d
    })

print(f"{'Campaign':<35} | {'Yesterday Cost':<14} | {'Yesterday Regs':<14} | {'Yesterday CPA':<14} | {'7-Day Cost':<12} | {'7-Day Convs':<12} | {'7-Day CPA':<12}")
print('-'*125)
for r in results:
    cpa_7d_str = f"${r['7d_cpa']:.2f}" if r['7d_cpa'] != float('inf') else 'N/A'
    yd_cpa_str = f"${float(r['yd_cpa']):.2f}" if r['yd_cpa'] != 'N/A' else 'N/A'
    print(f"{r['name']:<35} | ${r['yd_cost']:<13.2f} | {r['yd_regs']:<14} | {yd_cpa_str:<14} | ${r['7d_cost']:<11.2f} | {r['7d_conv']:<12.1f} | {cpa_7d_str:<12}")
