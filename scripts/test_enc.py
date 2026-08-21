import csv
import glob

for fpath in glob.glob('scripts/*.csv'):
    print('File:', fpath)
    for enc in ['utf-8-sig', 'utf-8', 'gbk', 'gb18030']:
        try:
            with open(fpath, 'r', encoding=enc) as f:
                reader = csv.reader(f)
                h = next(reader)
                print(f"  Encoding {enc} success, Header: {h}")
                break
        except Exception as e:
            pass
