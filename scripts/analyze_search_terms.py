# -*- coding: utf-8 -*-
import json

with open('search_terms.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Keywords that are generally bad for B2B SaaS API tools
suspicious_words = [
    'interview', 'salary', 'jobs', 'career', 'resume', 'internship',
    'exam', 'certification', 'training', 'course', 'class', 'syllabus',
    'meaning', 'definition', 'what is', 'how to', 'tutorial',
    'crack', 'torrent', 'nulled', 'free download full version',
    'reddit', 'youtube', 'github issues', 'vs'
]

wasteful_terms = []
irrelevant_terms = []

for row in data:
    term = row['search_term'].lower()
    cost = row['cost']
    conv = row['conversions']
    
    # 1. High spend, 0 conversions
    if conv == 0 and cost >= 2.0:
        wasteful_terms.append(row)
        
    # 2. Suspicious intent
    elif any(word in term for word in suspicious_words) and conv == 0:
        irrelevant_terms.append(row)

wasteful_terms.sort(key=lambda x: x['cost'], reverse=True)
irrelevant_terms.sort(key=lambda x: x['cost'], reverse=True)

with open('C:\\Users\\bobzh\\.gemini\\antigravity-ide\\brain\\990235be-beb7-46e2-b8fd-0c1768653729\\implementation_plan.md', 'w', encoding='utf-8') as f:
    f.write('# 🔍 搜索词分析与否定建议\n\n')
    f.write('我排查了过去 30 天内产生消耗的 **4815** 个搜索词，为您筛选出以下需要优先否定的关键词。\n\n')
    
    f.write('## 🛑 高消耗且 0 转化 (建议精确否定 Exact Match)\n')
    f.write('这些词消耗超过了 $2.0，但毫无转化，纯属浪费预算。\n\n')
    f.write('| 搜索词 (Search Term) | Campaign | Cost | Clicks |\n')
    f.write('| :--- | :--- | :--- | :--- |\n')
    for row in wasteful_terms[:30]: # Top 30
        f.write(f"| `{row['search_term']}` | {row['campaign']} | ${row['cost']:.2f} | {row['clicks']} |\n")
        
    f.write('\n## ⚠️ 意图不相关 / 学习找工作意图 (建议词组否定 Phrase Match)\n')
    f.write('包含 tutorial, interview, salary, meaning 等非商业采购意图的词。\n\n')
    f.write('| 搜索词 (Search Term) | Campaign | Cost | Clicks |\n')
    f.write('| :--- | :--- | :--- | :--- |\n')
    for row in irrelevant_terms[:30]: # Top 30
        f.write(f"| `{row['search_term']}` | {row['campaign']} | ${row['cost']:.2f} | {row['clicks']} |\n")
    
    f.write('\n> [!IMPORTANT]\n')
    f.write('> 请您检查以上搜索词。如果确认要否定，**请回复“同意”或“执行”**，我将调用 API 自动帮您把这些词加到广告系列的否定词表里！\n')

print(f'Found {len(wasteful_terms)} wasteful and {len(irrelevant_terms)} irrelevant terms.')
