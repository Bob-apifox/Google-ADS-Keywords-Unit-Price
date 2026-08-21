import csv
from collections import defaultdict
import io

def read_csv_safe(path):
    for enc in ['utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'utf-16', 'utf-16-le', 'utf-16-be']:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
            if '\0' in content and not enc.startswith('utf-16'):
                continue
            reader = csv.DictReader(io.StringIO(content))
            return list(reader), enc
        except Exception:
            continue
    print(f"Failed to read {path}")
    return [], None

def main():
    kw_file = r'd:\Apidog Work\Google ADS Keywords Unit Price\keyword_unit_price\scripts\来源为google_search的关键词有效数据(周) (5).csv'
    src_file = r'd:\Apidog Work\Google ADS Keywords Unit Price\keyword_unit_price\scripts\来源为google_search的各渠道有效数据(周) (4).csv'
    geo_file = r'd:\Apidog Work\Google ADS Keywords Unit Price\keyword_unit_price\scripts\来源为google_search的国家有效数据(周) (5).csv'

    wk_last = '2026-6-29 - 2026-7-5'
    wk_this = '2026-7-6 - 2026-7-12'

    kw_rows, enc_kw = read_csv_safe(kw_file)
    src_rows, enc_src = read_csv_safe(src_file)
    geo_rows, enc_geo = read_csv_safe(geo_file)
    
    print(f"Encodings - KW: {enc_kw}, SRC: {enc_src}, GEO: {enc_geo}")
    print(f"KW Fields: {kw_rows[0].keys() if kw_rows else 'None'}")
    print(f"SRC Fields: {src_rows[0].keys() if src_rows else 'None'}")
    print(f"GEO Fields: {geo_rows[0].keys() if geo_rows else 'None'}")
    
    def parse_int(val):
        try:
            return int(val.replace(',', ''))
        except:
            return 0

    # Keywords Data
    total_reg = {wk_last: 0, wk_this: 0}
    total_val = {wk_last: 0, wk_this: 0}
    kw_data = defaultdict(lambda: {wk_last: [0, 0], wk_this: [0, 0]})
    
    for row in kw_rows[1:]: # skip header
        if len(row) < 4: continue
        wk = list(row.values())[0]
        kw = list(row.values())[1]
        reg = parse_int(list(row.values())[2])
        val = parse_int(list(row.values())[3])
        if wk in total_reg:
            total_reg[wk] += reg
            total_val[wk] += val
            kw_data[kw][wk][0] += reg
            kw_data[kw][wk][1] += val

    # Source Data
    src_data = defaultdict(lambda: {wk_last: [0, 0], wk_this: [0, 0]})
    for row in src_rows[1:]:
        if len(row) < 4: continue
        wk = list(row.values())[0]
        src = list(row.values())[1]
        reg = parse_int(list(row.values())[2])
        val = parse_int(list(row.values())[3])
        if wk in src_data:
            src_data[src][wk][0] += reg
            src_data[src][wk][1] += val

    # Geo Data
    geo_data = defaultdict(lambda: {wk_last: [0, 0], wk_this: [0, 0]})
    for row in geo_rows[1:]:
        if len(row) < 5: continue
        wk = list(row.values())[0]
        # In geo: week, source, country, reg, val
        geo = list(row.values())[2]
        reg = parse_int(list(row.values())[3])
        val = parse_int(list(row.values())[4])
        if wk in geo_data:
            geo_data[geo][wk][0] += reg
            geo_data[geo][wk][1] += val

    # Print Results
    print(f"\\n--- OVERALL ---")
    val_rate_last = (total_val[wk_last] / total_reg[wk_last] * 100) if total_reg[wk_last] else 0
    val_rate_this = (total_val[wk_this] / total_reg[wk_this] * 100) if total_reg[wk_this] else 0
    print(f"Last wk: Reg {total_reg[wk_last]}, Valid {total_val[wk_last]} ({val_rate_last:.2f}%)")
    print(f"This wk: Reg {total_reg[wk_this]}, Valid {total_val[wk_this]} ({val_rate_this:.2f}%)")
    print(f"Delta: Reg {total_reg[wk_this] - total_reg[wk_last]}, Valid {total_val[wk_this] - total_val[wk_last]}")

    print(f"\\n--- TOP DROPPING SOURCE (Reg) ---")
    src_list = []
    for src, data in src_data.items():
        delta = data[wk_this][0] - data[wk_last][0]
        if delta < 0:
            src_list.append((src, data[wk_last][0], data[wk_this][0], delta))
    src_list.sort(key=lambda x: x[3])
    for s in src_list[:10]:
        print(f"Source: {s[0]} | Last: {s[1]} | This: {s[2]} | Delta: {s[3]}")

    print(f"\\n--- TOP DROPPING GEO (Reg) ---")
    geo_list = []
    for geo, data in geo_data.items():
        delta = data[wk_this][0] - data[wk_last][0]
        if delta < 0:
            geo_list.append((geo, data[wk_last][0], data[wk_this][0], delta))
    geo_list.sort(key=lambda x: x[3])
    for s in geo_list[:10]:
        print(f"Geo: {s[0]} | Last: {s[1]} | This: {s[2]} | Delta: {s[3]}")

    print(f"\\n--- TOP DROPPING KEYWORDS (Reg) ---")
    kw_list = []
    for kw, data in kw_data.items():
        delta = data[wk_this][0] - data[wk_last][0]
        if delta < 0:
            kw_list.append((kw, data[wk_last][0], data[wk_this][0], delta))
    kw_list.sort(key=lambda x: x[3])
    for s in kw_list[:10]:
        print(f"KW: {s[0]} | Last: {s[1]} | This: {s[2]} | Delta: {s[3]}")

if __name__ == '__main__':
    main()
