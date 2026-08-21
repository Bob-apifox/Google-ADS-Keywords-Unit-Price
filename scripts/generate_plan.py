import re
import os

with open('keyword_unit_price/reports/optimization_plan_2026-07-28.md', 'r', encoding='utf-8') as f:
    content = f.read()

negatives = {}
for match in re.finditer(r'## 🚩 重点优化对象: (.*?) \(`(.*?)`\).*?### 🔍 潜在浪费搜索词.*?\| :--- \|\n(.*?)(?=\n\n---|\Z)', content, re.DOTALL):
    camp_name = match.group(1).strip()
    table_content = match.group(3).strip()
    
    terms = []
    for line in table_content.split('\n'):
        if '暂无明显的浪费搜索词' in line:
            break
        parts = line.split('|')
        if len(parts) > 4:
            term = parts[1].strip().replace('`', '')
            cost = parts[2].strip()
            terms.append((term, cost))
    if terms:
        negatives[camp_name] = terms

plan = """# 28号数据深度优化方案 (2026-07-29执行)

基于 `run_report.bat` 跑出的数据，我为你制定了今天的账户级微调计划，请过目。

## User Review Required

> [!IMPORTANT]
> 以下计划涉及添加全局和系列层级的否定词（Negative Keywords），并暂停无效的高消耗词和广告组。请确认是否全部执行，或者有某些词你希望保留。

## Proposed Changes

### 1. 添加否定词 (Negative Keywords)
将以下高消耗无转化的冗余搜索词精准封杀，减少每日预算浪费。

"""

for camp, terms in negatives.items():
    plan += f'#### [MODIFY] Campaign: {camp}\n'
    for term, cost in terms:
        plan += f'- ➕ 添加精准否定词: `[{term}]` (昨日白白浪费 {cost})\n'
    plan += '\n'

plan += """### 2. 暂停高耗低效广告组 (Pause Inefficient Ad Groups)
- 针对 `Google-Sa-CLI-Global` 里的 `Terminal-Native-Clients` (消耗 $40.88, 0转化) 建议直接暂停。
- 针对 `Google-Sa-Func-AdvancedMock-Global` 里的 `Service-Virtualization` (消耗 $18.51, 0转化) 建议直接暂停。
- 针对 `Google-Sa-Stoplight-Global` 里的 `Stoplight-Features--Global` (CPA $5.10 远超基准) 降价或暂停。

## Verification Plan

### Automated Tests
- 运行自动化脚本把上述 Negative Keywords 注入各个 Campaign 的 Negative Keyword List 中。
- 调用 Google Ads API 批量暂停表现不佳的 Ad Group 及其 Keywords。
"""

with open(r'C:\Users\bobzh\.gemini\antigravity-ide\brain\df619394-c984-4a1b-a06e-a4f08016a39a\implementation_plan.md', 'w', encoding='utf-8') as f:
    f.write(plan)
