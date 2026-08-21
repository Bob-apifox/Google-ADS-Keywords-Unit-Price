import csv
import glob
from collections import defaultdict

def run():
    csv_files = glob.glob('scripts/*.csv')
    ch_file = [f for f in csv_files if '各渠道' in f or 'ĸ' in f or '渠道' in f][0]
    geo_file = [f for f in csv_files if '国家' in f or 'Ĺ' in f][0]
    kw_file = [f for f in csv_files if '关键词' in f or 'Ĺؼ' in f][0]

    # 1. Channel summary
    sources = defaultdict(lambda: {'last_week': {'reg': 0, 'valid': 0}, 'this_week': {'reg': 0, 'valid': 0}})
    with open(ch_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        for r in reader:
            if not r: continue
            week = r[0]
            source = r[1]
            reg = int(r[2].replace(',', ''))
            valid = int(r[3].replace(',', ''))
            target = 'this_week' if ('8-3' in week or '2026-8-3' in week) else 'last_week'
            sources[source][target]['reg'] += reg
            sources[source][target]['valid'] += valid

    print("=== FULL CHANNEL BREAKDOWN ===")
    total_lw_r = sum(v['last_week']['reg'] for v in sources.values())
    total_lw_v = sum(v['last_week']['valid'] for v in sources.values())
    total_tw_r = sum(v['this_week']['reg'] for v in sources.values())
    total_tw_v = sum(v['this_week']['valid'] for v in sources.values())

    print(f"Total Last Week: Reg={total_lw_r}, Valid={total_lw_v}, Rate={total_lw_v/total_lw_r*100:.2f}%")
    print(f"Total This Week: Reg={total_tw_r}, Valid={total_tw_v}, Rate={total_tw_v/total_tw_r*100:.2f}%")
    print(f"Delta: Reg={total_tw_r-total_lw_r:+d} ({(total_tw_r-total_lw_r)/total_lw_r*100:+.2f}%), Valid={total_tw_v-total_lw_v:+d} ({(total_tw_v-total_lw_v)/total_lw_v*100:+.2f}%), Rate Delta={total_tw_v/total_tw_r*100 - total_lw_v/total_lw_r*100:+.2f}%")

    ch_list = []
    for s, v in sources.items():
        lwr, lwv = v['last_week']['reg'], v['last_week']['valid']
        twr, twv = v['this_week']['reg'], v['this_week']['valid']
        dr = twr - lwr
        dv = twv - lwv
        pr = (dr / lwr * 100) if lwr > 0 else (100.0 if twr > 0 else 0)
        pv = (dv / lwv * 100) if lwv > 0 else (100.0 if twv > 0 else 0)
        l_rate = lwv / lwr * 100 if lwr else 0
        t_rate = twv / twr * 100 if twr else 0
        ch_list.append((s, lwr, twr, dr, pr, lwv, twv, dv, pv, l_rate, t_rate))

    print("\n--- Channels Sorted by Valid Drop (Worst first) ---")
    for r in sorted(ch_list, key=lambda x: x[7]):
        print(f"{r[0]:<20} | LW Reg: {r[1]:<5} | TW Reg: {r[2]:<5} | Reg Delta: {r[3]:<+6} ({r[4]:<+6.1f}%) | LW Val: {r[5]:<4} | TW Val: {r[6]:<4} | Val Delta: {r[7]:<+5} ({r[8]:<+6.1f}%) | LW Rate: {r[9]:<5.1f}% | TW Rate: {r[10]:<5.1f}%")

    # 2. Keywords
    kw_data = defaultdict(lambda: {'last_week': {'reg': 0, 'valid': 0}, 'this_week': {'reg': 0, 'valid': 0}})
    with open(kw_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        for r in reader:
            if not r: continue
            week = r[0]
            term = r[1]
            reg = int(r[2].replace(',', ''))
            valid = int(r[3].replace(',', ''))
            target = 'this_week' if ('8-3' in week or '2026-8-3' in week) else 'last_week'
            kw_data[term][target]['reg'] += reg
            kw_data[term][target]['valid'] += valid

    kw_rows = []
    for t, v in kw_data.items():
        lwr, lwv = v['last_week']['reg'], v['last_week']['valid']
        twr, twv = v['this_week']['reg'], v['this_week']['valid']
        dr = twr - lwr
        dv = twv - lwv
        pr = (dr / lwr * 100) if lwr > 0 else (100.0 if twr > 0 else 0)
        pv = (dv / lwv * 100) if lwv > 0 else (100.0 if twv > 0 else 0)
        l_rate = lwv / lwr * 100 if lwr else 0
        t_rate = twv / twr * 100 if twr else 0
        kw_rows.append((t, lwr, twr, dr, pr, lwv, twv, dv, pv, l_rate, t_rate))

    print("\n=== TOP 25 DROPS IN VALID USERS (KEYWORDS) ===")
    for r in sorted(kw_rows, key=lambda x: x[7])[:25]:
        print(f"{r[0]:<35} | Reg: {r[1]} -> {r[2]} ({r[3]:+d}) | Val: {r[5]} -> {r[6]} ({r[7]:+d}, {r[8]:+.1f}%) | Rate: {r[9]:.1f}% -> {r[10]:.1f}%")

    print("\n=== TOP 25 DROPS IN REGISTRATIONS (KEYWORDS) ===")
    for r in sorted(kw_rows, key=lambda x: x[3])[:25]:
        print(f"{r[0]:<35} | Reg: {r[1]} -> {r[2]} ({r[3]:+d}, {r[4]:+.1f}%) | Val: {r[5]} -> {r[6]} ({r[7]:+d}) | Rate: {r[9]:.1f}% -> {r[10]:.1f}%")

run()
