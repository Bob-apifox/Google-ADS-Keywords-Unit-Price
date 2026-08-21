import csv
import io

def read_csv_safe(path):
    for enc in ['utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'utf-16']:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
            if '\0' in content and not enc.startswith('utf-16'):
                continue
            reader = csv.DictReader(io.StringIO(content))
            return list(reader), enc
        except Exception:
            continue
    return [], None

def parse_int(val):
    try:
        return int(val.replace(',', ''))
    except:
        return 0

def main():
    kw_file = r'd:\Apidog Work\Google ADS Keywords Unit Price\keyword_unit_price\scripts\来源为google_search的关键词有效数据(周) (5).csv'
    kw_rows, _ = read_csv_safe(kw_file)
    
    # Define expanded keywords based on image (partial match or exact)
    expanded_kws = [
        "vscode", "plugin", "extension", "thunder client", 
        "offline", "open source alternative", "export postman", "migrate from postman",
        "llm", "openai", "langchain", "ai agent", "mcp", "model context protocol",
        "grpc", "websocket", "graphql"
    ]
    
    wk_this = '2026-7-6 - 2026-7-12'
    
    results = []
    
    for row in kw_rows[1:]:
        if len(row) < 4: continue
        wk = list(row.values())[0]
        if wk != wk_this: continue
        
        kw = list(row.values())[1].lower()
        reg = parse_int(list(row.values())[2])
        val = parse_int(list(row.values())[3])
        
        for e_kw in expanded_kws:
            if e_kw in kw:
                results.append((e_kw, kw, reg, val))
                break
                
    results.sort(key=lambda x: x[2], reverse=True)
    
    print("--- NEW EXPANDED KEYWORDS PERFORMANCE (This Week) ---")
    total_reg = 0
    total_val = 0
    for res in results:
        print(f"Theme: {res[0]} | KW: {res[1]} | Reg: {res[2]} | Val: {res[3]}")
        total_reg += res[2]
        total_val += res[3]
        
        
    print(f"\\nTOTAL from expanded: Reg {total_reg}, Val {total_val}")

if __name__ == '__main__':
    main()
