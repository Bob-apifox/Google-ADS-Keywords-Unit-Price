# -*- coding: utf-8 -*-
import json

with open('search_terms.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

suspicious_words = [
    'interview', 'salary', 'jobs', 'career', 'resume', 'internship',
    'exam', 'certification', 'training', 'course', 'class', 'syllabus',
    'meaning', 'definition', 'what is', 'how to', 'tutorial',
    'crack', 'torrent', 'nulled', 'free download full version',
    'reddit', 'youtube', 'github issues', 'vs'
]

irrelevant_terms = []

for row in data:
    term = row['search_term'].lower()
    conv = row['conversions']
    
    if any(word in term for word in suspicious_words) and conv == 0:
        irrelevant_terms.append(row)

irrelevant_terms.sort(key=lambda x: x['cost'], reverse=True)

with open('C:\\Users\\bobzh\\.gemini\\antigravity-ide\\brain\\990235be-beb7-46e2-b8fd-0c1768653729\\implementation_plan.md', 'w', encoding='utf-8') as f:
    f.write('# 🔍 搜索词分析：不相关意图词\n\n')
    f.write('按照您的要求，我目前**仅过滤出了意图明显不相关（如学习、找工作、寻找破解版等）且过去 30 天 0 转化**的搜索词。\n\n')
    
    f.write('## ⚠️ 建议添加为广泛/词组否定的词 (Phrase Match)\n')
    f.write('这些搜索词包含了 `tutorial`, `interview`, `salary`, `meaning` 等非商业意图词汇。建议我们在 Campaign 级别把这些具体的单词（如 interview, tutorial 等）作为广泛或词组匹配的否定词加进去，从而一劳永逸地屏蔽这类流量。\n\n')
    
    f.write('| 搜索词 (Search Term) | Campaign | Cost | Clicks |\n')
    f.write('| :--- | :--- | :--- | :--- |\n')
    for row in irrelevant_terms[:50]: # Top 50
        f.write(f"| `{row['search_term']}` | {row['campaign']} | ${row['cost']:.2f} | {row['clicks']} |\n")
    
    f.write('\n> [!IMPORTANT]\n')
    f.write('> 请您检查上述表格中的词汇。如果这些词确实对我们没有转化价值，**请回复“执行”**，我将编写脚本，把识别出的无关单词统一加入否定词库！\n')

print(f'Processed {len(irrelevant_terms)} irrelevant terms.')
