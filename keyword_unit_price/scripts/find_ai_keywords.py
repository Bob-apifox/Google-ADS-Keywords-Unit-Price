import re
import os

def extract_ai_keywords():
    report_file = r"d:\Apidog Work\Google ADS Keywords Unit Price\keyword_unit_price\reports\optimization_plan_2026-07-15.md"
    
    ai_patterns = ['ai', 'llm', 'gpt', 'agent', 'schema generator', 'copilot', 'model', 'context protocol', 'mcp']
    
    candidates = []
    
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all keyword tables
    # Format: | `keyword` | Quality Score | Cost | Conversions | Clicks | Status |
    keyword_lines = re.findall(r'\|\s*`([^`]+)`\s*\|[^|]+\|\s*\$([0-9.]+)\s*\|\s*([0-9.]+)\s*\|', content)
    
    for kw, cost, convs in keyword_lines:
        cost = float(cost)
        convs = float(convs)
        
        is_ai = any(p in kw.lower() for p in ai_patterns)
        
        if is_ai and convs > 0:
            candidates.append({
                "keyword": kw,
                "cost": cost,
                "conversions": convs,
                "cpa": cost / convs if convs > 0 else 0
            })
            
    # Deduplicate and sort by conversions
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c['keyword'] not in seen:
            seen.add(c['keyword'])
            unique_candidates.append(c)
            
    unique_candidates.sort(key=lambda x: x['conversions'], reverse=True)
    
    print("--- Top AI Converting Keywords ---")
    for c in unique_candidates:
        print(f"Keyword: {c['keyword']:<35} | Convs: {c['conversions']:>6.1f} | Cost: ${c['cost']:>5.2f} | CPA: ${c['cpa']:>5.2f}")

if __name__ == "__main__":
    extract_ai_keywords()
