# Read read_by_hand.txt (year item value, with # comments) and write data.json. Run: venv/bin/python figures.py
# Hartridge's accounts are short, so the figures are read by eye from the scans, not by an automatic reader. The checks:
# from 2019 the cost lines add up to total spending (within 2: the accounts round each line).
import json, pathlib, collections
here = pathlib.Path(__file__).parent
LINES = ['admin', 'utilities', 'motor', 'welfare', 'phone', 'estate', 'equipsundry', 'accountancy']
data = collections.defaultdict(dict)
for line in (here / 'read_by_hand.txt').read_text(encoding='utf-8').splitlines():
    p = line.split('#')[0].split()
    if len(p) == 3:
        data[int(p[0])][p[1]] = int(p[2].replace(',', ''))
checks = []
for y, d in sorted(data.items()):
    if 'admin' in d:
        s = sum(d[k] for k in LINES)
        if abs(s - d['spending']) > 2:
            checks.append(f'{y}: cost lines add up to {s:,}, total spending {d["spending"]:,}')
json.dump({y: data[y] for y in sorted(data)}, open(here / 'data.json', 'w'), indent=1)
print('Years:', min(data), '-', max(data))
print(f'Checks ({len(checks)})')
for c in checks:
    print('  ' + c)
if checks:
    raise SystemExit(1)
