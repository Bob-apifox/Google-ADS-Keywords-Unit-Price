
import json
with open('ag_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

md = '## 动态 CPA 建议值明细\n\n'
md += '| Campaign | Ad Group | Cost | Conversions | Actual CPA | 建议 Target CPA (x1.2) |\n'
md += '| :--- | :--- | :--- | :--- | :--- | :--- |\n'
for row in sorted(data, key=lambda x: x['campaign_name']):
    cost = row['cost']
    conv = row['conversions']
    cpa = row['actual_cpa']
    if conv > 0:
        target = min(cpa * 1.2, 2.5)
        target = max(target, 0.5)
        suggestion = f''
    else:
        suggestion = '.50'
    cpa_str = f'' if conv > 0 else 'N/A'
    cname = row['campaign_name']
    agname = row['ad_group_name']
    md += f'| {cname} | {agname} |  | {conv:.2f} | {cpa_str} | **{suggestion}** |\n'

with open('dynamic_cpa_table.md', 'w', encoding='utf-8') as f:
    f.write(md)


