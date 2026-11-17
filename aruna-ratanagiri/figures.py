# Read the figures out of txt/<year>.txt (made by extract.py) and write data.json.
#
# Harnham Buddhist Monastery Trust, years January to December. Every report is a Companies House scan read by text
# recognition, so digits can be misread. Each report gives its own year and the year before, so most years are
# read twice: from their own report and from the next report's "last year" column. Where the two agree the figure
# is taken; where only one can be read it is taken and noted; where they differ (or neither reads) the figure goes to
# the doubts list, to be checked on the scan. corrections.txt sets single figures by hand, each with its reason.
# Run: venv/bin/python figures.py
import json, pathlib, re, collections

here = pathlib.Path(__file__).parent
YEARS = sorted(int(p.stem) for p in (here / 'txt').glob('*.txt'))

# cost lines in the expenses notes ("Charitable activities", or before 2015 "Activities undertaken directly" plus
# "Support costs"); the same line name may come twice (restricted and unrestricted parts): they are added up.
COSTS = [
    ('staff', r'Staff costs'), ('rent', r'Rent (&|and) rates'), ('heat', r'Light (&|and) heat'),
    ('ins', r'Insurance'), ('repairs', r'Repairs'), ('office', r'(Postage|Office admin)'),
    ('phone', r'Telephone'), ('motor', r'Motor'), ('travel', r'(Travel|Traveiling|Study & travel)'),
    ('legal', r'Legal'), ('sundry', r'Sundry'), ('bank', r'Bank charges'), ('household', r'Household'),
    ('mbt', r'(?!x)x'),   # spending by the earlier trust (Magga Bhavaka Trust), 2011-12: set by hand, see read_by_hand.txt
    ('depr', r'Depreciation'), ('events', r'Events'), ('gov', r'Governance'), ('pubs', r'(FS )?[Pp]ublication'),
    ('religious', r'Items of religious'), ('disposal', r'(Profit|Loss).{0,6}disposal'),
    ('welfare', r'Bhikkhu Welfare'), ('breakfast', r'Breakfast'), ('misc', r'Miscellaneous'), ('dana', r'Dana'),
    ('kitchen', r'(Kitchen|Lockdown)'),
]
# single figures from the statement of financial activities (SOFA) and the balance sheet (BS)
CORE = [
    ('income', 'sofa', r'Total (incoming resources|income)'),
    ('spending', 'sofa', r'Total (resources expended|expenditure)\b(?! from)'),
    ('gov_sofa', 'sofa', r'Governance costs'),
]
# Not read yet: funds, cash and the balance sheet. The text reader can't place their columns reliably on these scans;
# read them by eye (read_by_hand.txt) if the page needs them.
STOP = r'total charitable activities expenditure|^\s*\d+\s+Trustees|^\s*Trustees\s*$|^\s*\d+\s+Employees'
NUM = re.compile(r'(?<![\w,.])[.(]?\d[\d,.;:]*\S*')


def value(tok):
    """'1,234' -> 1234, '(1,234)' -> -1234; None if the digits can't be read for sure."""
    t = tok.strip('.').replace(';', ',')
    m = re.fullmatch(r'(\()?(\d{1,3}(?:,\d{3})*)(\))?', t)
    if not m or bool(m.group(1)) != bool(m.group(3)):
        return None
    v = int(m.group(2).replace(',', ''))
    return -v if m.group(1) else v


def numbers(line):
    """[(end position, token)] for every number-like piece after the label; the label is the text before them."""
    out, label = [], line
    for m in NUM.finditer(line):
        if not out:
            label = line[:m.start()]
        out.append((m.end(), m.group()))
    return label.strip(' .:•-|'), out


def columns(lines, y):
    """End positions of the 'this year' and 'last year' columns: the two rightmost places where the numbers of
    named lines line up (the totals stand at the right of every table in these reports)."""
    for l in lines:                                    # a heading line with both years, if there is one
        a = re.search(rf'(?<!\d){y}(?!\d)', l)
        b = re.search(rf'(?<!\d){y - 1}(?!\d)', l)
        if a and b and a.end() < b.start() and len(re.findall(r'[A-Za-z]', l)) <= 12:
            return a.end(), b.end()
    ends = sorted(end for l in lines for end, _ in numbers(l)[1] if numbers(l)[0])
    groups = []
    for e in ends:
        if groups and e - groups[-1][-1] <= 4:
            groups[-1].append(e)
        else:
            groups.append([e])
    groups = [g for g in groups if len(g) >= 3]
    if not groups:
        return None
    mid = lambda g: sorted(g)[len(g) // 2]
    if len(groups) == 1:
        return (mid(groups[0]), 10 ** 6)
    return (mid(groups[-2]), mid(groups[-1]))


def read_block(lines, y, keys, cols=None, first_only=False):
    """Lines of one note or statement -> {key: (this year, last year)} with None for an unreadable figure."""
    out = collections.defaultdict(lambda: [0, 0])
    seen = collections.defaultdict(lambda: [False, False])
    cols = cols or columns(lines, y)
    if not cols:
        return {}, []
    unknown, done = [], set()
    for l in lines:
        label, nums = numbers(l)
        if not nums or not label:
            if nums and not label:
                unknown.append(l.strip())
            continue
        key = next((k for k, pat in keys if re.match(pat, label, re.I)), None)
        if not key or (first_only and key in done):
            continue
        done.add(key)
        for end, tok in nums:
            d = [abs(end - c) for c in cols]
            i = d.index(min(d))
            if min(d) > 8:
                continue                               # an unrestricted or restricted column, not a total
            v = value(tok)
            if out[key][i] is not None:
                out[key][i] = None if v is None else out[key][i] + v
            seen[key][i] = True
    return {k: tuple(v if seen[k][i] else None for i, v in enumerate(out[k])) for k in out}, unknown


def section(text, start, stop):
    """Lines from the first line matching start to the next matching stop."""
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if re.search(start, l):
            for j in range(i + 1, len(lines)):
                if re.search(stop, lines[j]):
                    return lines[i:j]
            return lines[i:]
    return []


readings = collections.defaultdict(dict)    # (year, key) -> {report year: value}
notes = []
for y in YEARS:
    t = (here / 'txt' / f'{y}.txt').read_text(encoding='utf-8')
    blocks = []
    # SOFA: from its heading to the balance sheet heading
    sofa = section(t, r'STATEMENT OF FINANCIAL ACTIVITIES', r'BALANCE SHEET')
    bs = section(t, r'BALANCE SHEET', r'NOTES TO THE|approved by|Company Registration')
    if y >= 2015:
        costs = section(t, r'^\s*\d+\s+Charitable activities\s*$', STOP)
    else:
        costs = (section(t, r'Activities undertaken directly', r'Support costs')
                 + section(t, r'Support costs\s*$', STOP))
    got = {}
    for name, lines, keys in [('sofa', sofa, [(k, p) for k, s, p in CORE if s == 'sofa']),
                              ('bs', bs, [(k, p) for k, s, p in CORE if s == 'bs']),
                              ('costs', costs, COSTS)]:
        r, unknown = read_block(lines, y, keys, first_only=name != 'costs')
        if not r:
            notes.append(f'{y}: no {name} columns found')
        for l in unknown:
            notes.append(f'{y} {name}: numbers with no line name: {l[:90]}')
        for k, (a, b) in r.items():
            if a is not None or k in got:
                readings[(y, k)][y] = a
            if b is not None and y - 1 >= YEARS[0]:
                readings[(y - 1, k)][y] = b

# settle each figure from its readings
data, doubts, single, settled = collections.defaultdict(dict), [], [], []
for (y, k), r in sorted(readings.items()):
    vals = {ry: v for ry, v in r.items() if v is not None}
    if len(set(vals.values())) == 1:
        data[y][k] = next(iter(vals.values()))
        if len(r) == 1 or len(vals) < len(r):
            single.append((y, k, r))
    elif r.get(y + 1) is not None:
        # the next report's "last year" column is always the rightmost one, so its reading is the safer
        data[y][k] = r[y + 1]
        settled.append((y, k, r))
    else:
        doubts.append((y, k, r))

hand = collections.defaultdict(dict)
for line in (here / 'read_by_hand.txt').read_text(encoding='utf-8').splitlines():
    line = line.split('#')[0].split()
    if len(line) == 3:
        y, k, v = int(line[0]), line[1], value(line[2])
        hand[y][k] = hand[y].get(k, 0) + v
cost_keys = {k for k, _ in COSTS}
differ = []
for y, d in hand.items():
    for k in (set(d) | {k for k in data[y] if k in cost_keys}) if any(k in cost_keys for k in d) else set(d) - cost_keys:
        if data[y].get(k) not in (None, d.get(k)) or (k not in d and data[y].get(k)):
            differ.append(f'{y} {k}: by eye {d.get(k, 0):,}, automatic {data[y].get(k)}')
    if any(k in cost_keys for k in d):                 # the eye read this year's cost lines: they replace the reader's
        for k in [k for k in data[y] if k in cost_keys]:
            del data[y][k]
    data[y].update(d)
    doubts = [x for x in doubts if not (x[0] == y and x[1] in cost_keys)]
for line in (here / 'corrections.txt').read_text(encoding='utf-8').splitlines() if (here / 'corrections.txt').exists() else []:
    line = line.split('#')[0].split()
    if len(line) == 3:
        data[int(line[0])][line[1]] = value(line[2])
        doubts = [d for d in doubts if (d[0], d[1]) != (int(line[0]), line[1])]

# checks: the cost lines add up to total spending (where the statement's total couldn't be read, the lines give it)
checks = []
for y in YEARS:
    d = data[y]
    lines = sum(d.get(k, 0) for k, _ in COSTS)
    if y < 2015 and 'gov' not in d:
        lines += d.get('gov_sofa', 0)
    if 'spending' not in d and lines:
        d['spending'] = lines
        notes.append(f'{y}: total spending taken from the cost lines ({lines:,})')
    if 'spending' in d and abs(lines - d['spending']) > 2:     # the notes round to within £2 of the statement
        checks.append(f'{y}: cost lines add up to {lines:,}, total spending {d["spending"]:,} (off by {d["spending"] - lines:,})')

json.dump({y: data[y] for y in sorted(data)}, open(here / 'data.json', 'w'), indent=1)
print('Years:', ', '.join(map(str, sorted(data))))
print(f'\nDoubts ({len(doubts)}): the readings differ or neither can be read')
for y, k, r in doubts:
    print(f'  {y} {k}: ' + ', '.join(f'{ry} report: {v if v is not None else "unreadable"}' for ry, v in sorted(r.items())))
print(f'\nSettled by the next report ({len(settled)}): its last-year column is used')
for y, k, r in settled:
    print(f'  {y} {k}: ' + ', '.join(f'{ry} report: {v if v is not None else "unreadable"}' for ry, v in sorted(r.items())))
print(f'\nRead once only ({len(single)})')
for y, k, r in single:
    print(f'  {y} {k}: ' + ', '.join(f'{ry}: {v}' for ry, v in sorted(r.items())))
notes = [n for n in notes if 'no line name' not in n and not n.startswith('2009')]
print(f'\nNotes ({len(notes)})')
for n in notes:
    print('  ' + n)
print(f'\nAutomatic reader differs from the eye ({len(differ)}), for information')
for x in differ:
    print('  ' + x)
print(f'\nChecks ({len(checks)})')
for c in checks:
    print('  ' + c)
