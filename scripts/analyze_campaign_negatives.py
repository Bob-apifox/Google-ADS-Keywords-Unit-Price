# -*- coding: utf-8 -*-
import json

with open('search_terms.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

suspicious_words = [
    'interview', 'salary', 'jobs', 'career', 'resume', 'internship',
    'exam', 'certification', 'training', 'course', 'class', 'syllabus',
    'meaning', 'definition', 'what is', 'how to', 'tutorial',
    'crack', 'torrent', 'nulled', 'free download full version',
    'reddit', 'youtube', 'github issues', 'vs', 'difference between'
]

campaigns_data = {}

for row in data:
    term = row['search_term'].lower()
    conv = row['conversions']
    cost = row['cost']
    camp = row['campaign']
    
    if camp not in campaigns_data:
        campaigns_data[camp] = {'irrelevant': [], 'wasteful': []}
        
    if any(word in term for word in suspicious_words) and conv == 0:
        campaigns_data[camp]['irrelevant'].append(row)

with open('C:\\Users\\bobzh\\.gemini\\antigravity-ide\\brain\\990235be-beb7-46e2-b8fd-0c1768653729\\implementation_plan.md', 'w', encoding='utf-8') as f:
    f.write('# 🎯 各 Campaign 否定关键词专属计划\n\n')
    f.write('按照您的要求，我逐个排查了所有 Campaign 的真实搜索词，并针对每个 Campaign 整理了专门的**不相关词汇（求职、学习、对比等）**否定列表。\n\n')
    
    for camp, lists in sorted(campaigns_data.items()):
        irrelevant = lists['irrelevant']
        if not irrelevant:
            continue
            
        irrelevant.sort(key=lambda x: x['cost'], reverse=True)
        
        f.write(f'## 📦 {camp}\n')
        f.write('**建议添加的否定词组 (Phrase Match):**\n')
        
        roots_to_negate = set()
        for row in irrelevant:
            term = row['search_term'].lower()
            for w in suspicious_words:
                if w in term:
                    roots_to_negate.add(w)
                    
        f.write('基于以下搜索词，建议在此 Campaign 中添加以下核心词作为**广泛/词组否定**：\n')
        roots_str = '`, `'.join(roots_to_negate)
        f.write(f"> `{roots_str}`\n\n")
        
        f.write('| 触发的不相关搜索词 | 花费 (USD) | 点击 |\n')
        f.write('| :--- | :--- | :--- |\n')
        
        for row in irrelevant[:15]:
            f.write(f"| `{row['search_term']}` | ${row['cost']:.2f} | {row['clicks']} |\n")
        f.write('\n---\n\n')
        
    f.write('> [!IMPORTANT]\n')
    f.write('> 请您检查上方每个 Campaign 的否词计划。如果方向准确，**请回复“执行”**，我将直接通过 API 帮您把这些核心否定词注入到各自的 Campaign 设置中！\n')

print('Generated campaign-level negative keyword plan.')
