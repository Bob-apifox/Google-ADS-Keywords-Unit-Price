import csv
import glob
from collections import defaultdict

def run():
    csv_files = glob.glob('scripts/*.csv')
    ch_file = [f for f in csv_files if '各渠道' in f or 'ĸ' in f or '渠道' in f][0]
    geo_file = [f for f in csv_files if '国家' in f or 'Ĺ' in f][0]
    kw_file = [f for f in csv_files if '关键词' in f or 'Ĺؼ' in f][0]

    print(f"Channel file: {ch_file}")
    print(f"Geo file: {geo_file}")
    print(f"Keyword file: {kw_file}")

    # 1. Channels
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

    print("\n" + "="*80)
    print("ALL CHANNELS SUMMARY")
    print("="*80)
    total_lw_r = sum(v['last_week']['reg'] for v in sources.values())
    total_lw_v = sum(v['last_week']['valid'] for v in sources.values())
    total_tw_r = sum(v['this_week']['reg'] for v in sources.values())
    total_tw_v = sum(v['this_week']['valid'] for v in sources.values())

    print(f"Total Last Week (2026-7-27 ~ 8-2): Reg = {total_lw_r:,}, Valid = {total_lw_v:,}, Valid Rate = {total_lw_v/total_lw_r*100:.2f}%")
    print(f"Total This Week (2026-8-3 ~ 8-9):  Reg = {total_tw_r:,}, Valid = {total_tw_v:,}, Valid Rate = {total_tw_v/total_tw_r*100:.2f}%")
    print(f"Registration Change: {total_tw_r - total_lw_r:+d} ({(total_tw_r-total_lw_r)/total_lw_r*100:+.2f}%)")
    print(f"Valid Users Change:  {total_tw_v - total_lw_v:+d} ({(total_tw_v-total_lw_v)/total_lw_v*100:+.2f}%)")
    print(f"Valid Rate Change:   {total_tw_v/total_tw_r*100 - total_lw_v/total_lw_r*100:+.2f}%")

    print("\n" + "-"*130)
    print(f"{'Source':<20} | {'LW Reg':<8} | {'TW Reg':<8} | {'Reg Delta':<10} | {'Reg WoW%':<10} | {'LW Val':<8} | {'TW Val':<8} | {'Val Delta':<10} | {'Val WoW%':<10} | {'LW Rate':<8} | {'TW Rate':<8}")
    print("-"*130)
    
    ch_rows = []
    for s, v in sources.items():
        lwr, lwv = v['last_week']['reg'], v['last_week']['valid']
        twr, twv = v['this_week']['reg'], v['this_week']['valid']
        dr = twr - lwr
        dv = twv - lwv
        pr = (dr / lwr * 100) if lwr > 0 else (100.0 if twr > 0 else 0)
        pv = (dv / lwv * 100) if lwv > 0 else (100.0 if twv > 0 else 0)
        l_rate = lwv / lwr * 100 if lwr else 0
        t_rate = twv / twr * 100 if twr else 0
        ch_rows.append((s, lwr, twr, dr, pr, lwv, twv, dv, pv, l_rate, t_rate))

    # Sort by valid users delta ascending (biggest loss first)
    for row in sorted(ch_rows, key=lambda x: x[7]):
        print(f"{row[0]:<20} | {row[1]:<8} | {row[2]:<8} | {row[3]:<+10} | {row[4]:<+9.2f}% | {row[5]:<8} | {row[6]:<8} | {row[7]:<+10} | {row[8]:<+9.2f}% | {row[9]:<7.2f}% | {row[10]:<7.2f}%")

    # 2. Geo breakdown
    geo_data = defaultdict(lambda: defaultdict(lambda: {'last_week': {'reg': 0, 'valid': 0}, 'this_week': {'reg': 0, 'valid': 0}}))
    with open(geo_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        for r in reader:
            if not r: continue
            week = r[0]
            source = r[1]
            country = r[2]
            reg = int(r[3].replace(',', ''))
            valid = int(r[4].replace(',', ''))
            target = 'this_week' if ('8-3' in week or '2026-8-3' in week) else 'last_week'
            geo_data[source][country][target]['reg'] += reg
            geo_data[source][country][target]['valid'] += valid

    print("\n" + "="*80)
    print("GEO BREAKDOWN (BY SOURCE)")
    print("="*80)
    for src in sorted(geo_data.keys()):
        print(f"\n--- Source: {src} ---")
        g_rows = []
        for c, v in geo_data[src].items():
            lwr, lwv = v['last_week']['reg'], v['last_week']['valid']
            twr, twv = v['this_week']['reg'], v['this_week']['valid']
            dr = twr - lwr
            dv = twv - lwv
            pr = (dr / lwr * 100) if lwr > 0 else (100.0 if twr > 0 else 0)
            pv = (dv / lwv * 100) if lwv > 0 else (100.0 if twv > 0 else 0)
            l_rate = lwv / lwr * 100 if lwr else 0
            t_rate = twv / twr * 100 if twr else 0
            g_rows.append((c, lwr, twr, dr, pr, lwv, twv, dv, pv, l_rate, t_rate))
        
        print(f"Top 10 drops in VALID USERS for {src}:")
        print(f"{'Country':<10} | {'LW Reg':<8} | {'TW Reg':<8} | {'Reg Delta':<10} | {'LW Val':<8} | {'TW Val':<8} | {'Val Delta':<10} | {'Val WoW%':<10} | {'LW Rate':<8} | {'TW Rate':<8}")
        print("-"*110)
        for row in sorted(g_rows, key=lambda x: x[7])[:10]:
            print(f"{row[0]:<10} | {row[1]:<8} | {row[2]:<8} | {row[3]:<+10} | {row[5]:<8} | {row[6]:<8} | {row[7]:<+10} | {row[8]:<+9.2f}% | {row[9]:<7.2f}% | {row[10]:<7.2f}%")

        print(f"\nTop 10 GAINS in VALID USERS for {src}:")
        print(f"{'Country':<10} | {'LW Reg':<8} | {'TW Reg':<8} | {'Reg Delta':<10} | {'LW Val':<8} | {'TW Val':<8} | {'Val Delta':<10} | {'Val WoW%':<10} | {'LW Rate':<8} | {'TW Rate':<8}")
        print("-"*110)
        for row in sorted(g_rows, key=lambda x: x[7], reverse=True)[:10]:
            print(f"{row[0]:<10} | {row[1]:<8} | {row[2]:<8} | {row[3]:<+10} | {row[5]:<8} | {row[6]:<8} | {row[7]:<+10} | {row[8]:<+9.2f}% | {row[9]:<7.2f}% | {row[10]:<7.2f}%")

    # 3. Keywords
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

    print("\n" + "="*80)
    print("KEYWORD / UTM TERM BREAKDOWN (google_search)")
    print("="*80)
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

    print(f"Top 20 drops in VALID USERS by Keyword:")
    print(f"{'Utm Term':<35} | {'LW Reg':<8} | {'TW Reg':<8} | {'Reg Delta':<10} | {'LW Val':<8} | {'TW Val':<8} | {'Val Delta':<10} | {'Val WoW%':<10} | {'LW Rate':<8} | {'TW Rate':<8}")
    print("-"*125)
    for row in sorted(kw_rows, key=lambda x: x[7])[:20]:
        print(f"{row[0]:<35} | {row[1]:<8} | {row[2]:<8} | {row[3]:<+10} | {row[5]:<8} | {row[6]:<8} | {row[7]:<+10} | {row[8]:<+9.2f}% | {row[9]:<7.2f}% | {row[10]:<7.2f}%")

    print(f"\nTop 20 GAINS in VALID USERS by Keyword:")
    print(f"{'Utm Term':<35} | {'LW Reg':<8} | {'TW Reg':<8} | {'Reg Delta':<10} | {'LW Val':<8} | {'TW Val':<8} | {'Val Delta':<10} | {'Val WoW%':<10} | {'LW Rate':<8} | {'TW Rate':<8}")
    print("-"*125)
    for row in sorted(kw_rows, key=lambda x: x[7], reverse=True)[:20]:
        print(f"{row[0]:<35} | {row[1]:<8} | {row[2]:<8} | {row[3]:<+10} | {row[5]:<8} | {row[6]:<8} | {row[7]:<+10} | {row[8]:<+9.2f}% | {row[9]:<7.2f}% | {row[10]:<7.2f}%")

    print(f"\nTop 20 drops in REGISTRATIONS by Keyword:")
    print(f"{'Utm Term':<35} | {'LW Reg':<8} | {'TW Reg':<8} | {'Reg Delta':<10} | {'LW Val':<8} | {'TW Val':<8} | {'Val Delta':<10} | {'Val WoW%':<10} | {'LW Rate':<8} | {'TW Rate':<8}")
    print("-"*125)
    for row in sorted(kw_rows, key=lambda x: x[3])[:20]:
        print(f"{row[0]:<35} | {row[1]:<8} | {row[2]:<8} | {row[3]:<+10} | {row[5]:<8} | {row[6]:<8} | {row[7]:<+10} | {row[8]:<+9.2f}% | {row[9]:<7.2f}% | {row[10]:<7.2f}%")

    print(f"\nTop 20 GAINS in REGISTRATIONS by Keyword:")
    print(f"{'Utm Term':<35} | {'LW Reg':<8} | {'TW Reg':<8} | {'Reg Delta':<10} | {'LW Val':<8} | {'TW Val':<8} | {'Val Delta':<10} | {'Val WoW%':<10} | {'LW Rate':<8} | {'TW Rate':<8}")
    print("-"*125)
    for row in sorted(kw_rows, key=lambda x: x[3], reverse=True)[:20]:
        print(f"{row[0]:<35} | {row[1]:<8} | {row[2]:<8} | {row[3]:<+10} | {row[5]:<8} | {row[6]:<8} | {row[7]:<+10} | {row[8]:<+9.2f}% | {row[9]:<7.2f}% | {row[10]:<7.2f}%")

if __name__ == '__main__':
    run()
