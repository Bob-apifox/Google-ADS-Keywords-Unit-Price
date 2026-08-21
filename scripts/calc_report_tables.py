import csv
import glob
from collections import defaultdict

csv_files = glob.glob('scripts/*.csv')
ch_file = [f for f in csv_files if '各渠道' in f or 'ĸ' in f or '渠道' in f][0]
geo_file = [f for f in csv_files if '国家' in f or 'Ĺ' in f][0]
kw_file = [f for f in csv_files if '关键词' in f or 'Ĺؼ' in f][0]

# --- 1. CHANNEL DATA ---
sources = defaultdict(lambda: {'lw_r': 0, 'lw_v': 0, 'tw_r': 0, 'tw_v': 0})
with open(ch_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader)
    for r in reader:
        if not r: continue
        week = r[0]
        s = r[1]
        reg = int(r[2].replace(',', ''))
        val = int(r[3].replace(',', ''))
        if '8-3' in week or '2026-8-3' in week:
            sources[s]['tw_r'] += reg
            sources[s]['tw_v'] += val
        else:
            sources[s]['lw_r'] += reg
            sources[s]['lw_v'] += val

# --- 2. GEO DATA ---
geo = defaultdict(lambda: defaultdict(lambda: {'lw_r': 0, 'lw_v': 0, 'tw_r': 0, 'tw_v': 0}))
with open(geo_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader)
    for r in reader:
        if not r: continue
        week = r[0]
        s = r[1]
        c = r[2]
        reg = int(r[3].replace(',', ''))
        val = int(r[4].replace(',', ''))
        if '8-3' in week or '2026-8-3' in week:
            geo[s][c]['tw_r'] += reg
            geo[s][c]['tw_v'] += val
        else:
            geo[s][c]['lw_r'] += reg
            geo[s][c]['lw_v'] += val

# --- 3. KEYWORD DATA ---
kw = defaultdict(lambda: {'lw_r': 0, 'lw_v': 0, 'tw_r': 0, 'tw_v': 0})
with open(kw_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader)
    for r in reader:
        if not r: continue
        week = r[0]
        t = r[1]
        reg = int(r[2].replace(',', ''))
        val = int(r[3].replace(',', ''))
        if '8-3' in week or '2026-8-3' in week:
            kw[t]['tw_r'] += reg
            kw[t]['tw_v'] += val
        else:
            kw[t]['lw_r'] += reg
            kw[t]['lw_v'] += val

print("=== 1. BIG PICTURE ===")
tot_lw_r = sum(v['lw_r'] for v in sources.values())
tot_lw_v = sum(v['lw_v'] for v in sources.values())
tot_tw_r = sum(v['tw_r'] for v in sources.values())
tot_tw_v = sum(v['tw_v'] for v in sources.values())
print(f"LW: Reg = {tot_lw_r:,}, Valid = {tot_lw_v:,}, Rate = {tot_lw_v/tot_lw_r*100:.2f}%")
print(f"TW: Reg = {tot_tw_r:,}, Valid = {tot_tw_v:,}, Rate = {tot_tw_v/tot_tw_r*100:.2f}%")
print(f"Delta: Reg = {tot_tw_r - tot_lw_r:+d} ({(tot_tw_r - tot_lw_r)/tot_lw_r*100:+.2f}%), Valid = {tot_tw_v - tot_lw_v:+d} ({(tot_tw_v - tot_lw_v)/tot_lw_v*100:+.2f}%), Rate = {tot_tw_v/tot_tw_r*100 - tot_lw_v/tot_lw_r*100:+.2f}pp")

print("\n=== 2. CHANNELS (SORTED BY VALID USERS DROP) ===")
ch_rows = []
for s, v in sources.items():
    dr = v['tw_r'] - v['lw_r']
    dv = v['tw_v'] - v['lw_v']
    pr = (dr / v['lw_r'] * 100) if v['lw_r'] > 0 else (100.0 if v['tw_r'] > 0 else 0.0)
    pv = (dv / v['lw_v'] * 100) if v['lw_v'] > 0 else (100.0 if v['tw_v'] > 0 else 0.0)
    lwr = v['lw_v'] / v['lw_r'] * 100 if v['lw_r'] > 0 else 0
    twr = v['tw_v'] / v['tw_r'] * 100 if v['tw_r'] > 0 else 0
    ch_rows.append({
        's': s, 'lw_r': v['lw_r'], 'tw_r': v['tw_r'], 'dr': dr, 'pr': pr,
        'lw_v': v['lw_v'], 'tw_v': v['tw_v'], 'dv': dv, 'pv': pv,
        'lwr': lwr, 'twr': twr
    })

print("| 渠道 (Source) | 上周注册 | 本周注册 | 注册变化 (WoW%) | 上周有效 | 本周有效 | 有效变化 (WoW%) | 上周有效率 | 本周有效率 | 有效率变化 |")
print("|---|---|---|---|---|---|---|---|---|---|")
for c in sorted(ch_rows, key=lambda x: x['dv']):
    print(f"| `{c['s']}` | {c['lw_r']:,} | {c['tw_r']:,} | {c['dr']:+d} ({c['pr']:+.2f}%) | {c['lw_v']:,} | {c['tw_v']:,} | {c['dv']:+d} ({c['pv']:+.2f}%) | {c['lwr']:.2f}% | {c['twr']:.2f}% | {c['twr']-c['lwr']:+.2f}pp |")

print("\n=== 3. TOP COUNTRY DROPS IN GOOGLE_SEARCH (VALID USERS) ===")
geo_gs = []
for c, v in geo['google_search'].items():
    dr = v['tw_r'] - v['lw_r']
    dv = v['tw_v'] - v['lw_v']
    pr = (dr / v['lw_r'] * 100) if v['lw_r'] > 0 else (100.0 if v['tw_r'] > 0 else 0.0)
    pv = (dv / v['lw_v'] * 100) if v['lw_v'] > 0 else (100.0 if v['tw_v'] > 0 else 0.0)
    lwr = v['lw_v'] / v['lw_r'] * 100 if v['lw_r'] > 0 else 0
    twr = v['tw_v'] / v['tw_r'] * 100 if v['tw_r'] > 0 else 0
    geo_gs.append({
        'c': c, 'lw_r': v['lw_r'], 'tw_r': v['tw_r'], 'dr': dr, 'pr': pr,
        'lw_v': v['lw_v'], 'tw_v': v['tw_v'], 'dv': dv, 'pv': pv,
        'lwr': lwr, 'twr': twr
    })

print("| 国家代码 (Country) | 上周注册 | 本周注册 | 注册变化 (WoW%) | 上周有效 | 本周有效 | 有效变化 (WoW%) | 上周有效率 | 本周有效率 | 有效率变化 |")
print("|---|---|---|---|---|---|---|---|---|---|")
for g in sorted(geo_gs, key=lambda x: x['dv'])[:15]:
    print(f"| `{g['c']}` | {g['lw_r']:,} | {g['tw_r']:,} | {g['dr']:+d} ({g['pr']:+.2f}%) | {g['lw_v']:,} | {g['tw_v']:,} | {g['dv']:+d} ({g['pv']:+.2f}%) | {g['lwr']:.2f}% | {g['twr']:.2f}% | {g['twr']-g['lwr']:+.2f}pp |")

print("\n=== 4. TOP KEYWORD DROPS (VALID USERS) ===")
kw_list = []
for t, v in kw.items():
    dr = v['tw_r'] - v['lw_r']
    dv = v['tw_v'] - v['lw_v']
    pr = (dr / v['lw_r'] * 100) if v['lw_r'] > 0 else (100.0 if v['tw_r'] > 0 else 0.0)
    pv = (dv / v['lw_v'] * 100) if v['lw_v'] > 0 else (100.0 if v['tw_v'] > 0 else 0.0)
    lwr = v['lw_v'] / v['lw_r'] * 100 if v['lw_r'] > 0 else 0
    twr = v['tw_v'] / v['tw_r'] * 100 if v['tw_r'] > 0 else 0
    kw_list.append({
        't': t if t else '(empty / not set)', 'lw_r': v['lw_r'], 'tw_r': v['tw_r'], 'dr': dr, 'pr': pr,
        'lw_v': v['lw_v'], 'tw_v': v['tw_v'], 'dv': dv, 'pv': pv,
        'lwr': lwr, 'twr': twr
    })

print("| 关键词 (Utm Term) | 上周注册 | 本周注册 | 注册变化 (WoW%) | 上周有效 | 本周有效 | 有效变化 (WoW%) | 上周有效率 | 本周有效率 | 有效率变化 |")
print("|---|---|---|---|---|---|---|---|---|---|")
for k in sorted(kw_list, key=lambda x: x['dv'])[:20]:
    print(f"| `{k['t']}` | {k['lw_r']:,} | {k['tw_r']:,} | {k['dr']:+d} ({k['pr']:+.2f}%) | {k['lw_v']:,} | {k['tw_v']:,} | {k['dv']:+d} ({k['pv']:+.2f}%) | {k['lwr']:.2f}% | {k['twr']:.2f}% | {k['twr']-k['lwr']:+.2f}pp |")

print("\n=== 5. KEYWORD CLUSTERING & ANOMALIES ===")
# Let's inspect keywords with 0 valid users this week but high registrations (Traffic Wasters)
wasters = [k for k in kw_list if k['tw_v'] == 0 and k['tw_r'] >= 5]
print("\n--- Zero-Valid Wasters (TW Reg >= 5, Valid = 0) ---")
for w in sorted(wasters, key=lambda x: x['tw_r'], reverse=True):
    print(f"Term: {w['t']:<35} | Reg: {w['tw_r']} | Valid: 0 | Delta Reg: {w['dr']:+d}")

# Low valid rate wasters (TW Reg >= 20, Rate < 10%)
low_rate = [k for k in kw_list if k['tw_r'] >= 20 and k['twr'] < 10.0]
print("\n--- Low Valid Rate Terms (TW Reg >= 20, Valid Rate < 10%) ---")
for l in sorted(low_rate, key=lambda x: x['tw_r'], reverse=True):
    print(f"Term: {l['t']:<35} | Reg: {l['tw_r']} | Valid: {l['tw_v']} | Rate: {l['twr']:.2f}% | Delta Valid: {l['dv']:+d}")

# High potential winners (TW Valid >= 3, Rate >= 20%)
winners = [k for k in kw_list if k['tw_v'] >= 3 and k['twr'] >= 20.0]
print("\n--- High Performing Winners (TW Valid >= 3, Valid Rate >= 20%) ---")
for win in sorted(winners, key=lambda x: x['tw_v'], reverse=True):
    print(f"Term: {win['t']:<35} | Reg: {win['tw_r']} | Valid: {win['tw_v']} | Rate: {win['twr']:.2f}% | Delta Valid: {win['dv']:+d}")

