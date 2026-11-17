# Read the figures out of txt/<year>.txt (made by extract.py) and write data.json.
#
# Each report gives two columns: the year it is for and the year before. So most years are read twice,
# once from their own report and once from the next one. A year's figures come from its own report, except
# when that report is a scan (its text comes from character recognition and has misread digits); then the
# next report's "previous year" column is used. corrections.txt can set any single figure by hand.
# The checks at the end add up every total; run: venv/bin/python figures.py
import json, pathlib, re, sys

here = pathlib.Path(__file__).parent
# reports that are scans: the Trust's 2023 copy, and every year only found at Companies House.
# Their own figures are used after a clean copy (the next report's "previous year" column) where there is one.
SCANNED = {2023} | {int(re.search(r'\d{4}', p.stem).group()) for p in (here / 'accounts').glob('Companies_House_*.pdf')
                    if not any((here / 'accounts').glob(f'English_Sangha_Trust_*{re.search(r"\d{4}", p.stem).group()}*.pdf'))}
DETAIL_FROM = 2020        # the full set of figures is required from this year on; before it, only the CORE ones
CORE = ['income', 'spending', 'funds', 'buildings', 'cash']   # read for every year; the long-run charts use these

# where each section starts and ends (the group figures come before the company figures in every report)
SECTIONS = {
    # upper case only, so the contents page ("Statement of financial activities  9") doesn't count
    'sofa':  (r'^(CONSO\w+ )?STATEMENT OF FINANCIAL ACTIVITIES', r'COMPANY STATEMENT OF FINANCIAL|BALANCE SHEET'),
    'bs':    (r'^(CONSO\w+ )?BALANCE SHEET', r'COMPANY BALANCE SHEET|STATEMENT OF CASH FLOWS|NOTES TO THE'),
    'n2':    (r'INCOME FROM DONATIONS AND LEGACIES', r'INCOME FROM INVESTMENTS'),
    'n5':    (r'ANALYSIS OF EXPENDITURE ON CHARITABLE', r'GOVERNANCE COSTS\s*$'),
    'n3':    (r'INCOME FROM INVESTMENTS', r'OTHER INCOME'),
    'n10':   (r'STAFF COSTS AND EMPLOYEE', r'TANGIBLE FIXED ASSETS\s*$'),
    'n15':   (r'FUNDS MOVEMENT', r'SHARE CAPITAL|SUMMARY OF FUNDS|ANALYSIS OF NET ASSETS'),
    'n11':   (r'TANGIBLE FIXED ASSETS\s*$', r'INVESTMENTS\s*$'),
}
# key: (section, line label, how to read the numbers, optional?)
#   last2  = the last two numbers are this year and last year
#   note2  = six columns (unrestricted, restricted, total for each year), or four when the dashes were lost
#   staff  = number, FTE, number, FTE
#   one    = only this year (the last number)
#   unr6   = six columns as in note2; take the unrestricted ones (first and fourth)
ITEMS = {
    'donations':   ('sofa', r'Donations and legacies', 'last2', False),
    'interest':    ('sofa', r'Investments', 'last2', False),
    'other':       ('sofa', r'Other', 'last2', False),
    # the totals, with the names older reports use for them (labels may run over two lines)
    'income':      ('sofa', r'(Total income|TOTAL INCOME|Total incoming resources|TOTAL INCOMING( RESOURCES)?)', 'last2', False),
    'spending':    ('sofa', r'(Total expenditure|TOTAL EXPENDITURE|Total resources expended|TOTAL RESOURCES( EXPENDED)?)', 'last2', False),
    'gains':       ('sofa', r'Net gains', 'last2', True),
    'net':         ('sofa', r'(Net income|Net movement in funds|NET MOVEMENT IN( FUNDS)?)', 'last2', False),
    'funds':       ('sofa', r'(Total funds carried forward|TOTAL FUNDS AT 31|Total funds at 31)', 'last2', False),
    'gifts':       ('n2', r'Gifts', 'note2', False),
    'legacies':    ('n2', r'Legacies', 'note2', False),
    'gifts_u':     ('n2', r'Gifts', 'unr6', False),
    'interest_u':  ('n3', r'(Interest receivable|Investment income)', 'unr6', False),
    'buildings':   ('bs', r'(Tangible fixed assets|Tangible assets)', 'last2', False),
    'deposits':    ('bs', r'Short term deposits', 'last2', True),
    'investments': ('bs', r'Investments', 'last2', True),
    'debtors':     ('bs', r'Debtors', 'last2', False),
    'cash':        ('bs', r'Cash at bank', 'last2', False),
    'creditors':   ('bs', r'(Creditors:? amounts falling due within one year|due within one year)', 'last2', False),
    'net_assets':  ('bs', r'Net assets', 'last2', False),
    'restricted':  ('bs', r'Restricted funds', 'last2', False),
    'designated':  ('bs', r'Designated funds', 'last2', False),
    'general':     ('bs', r'General funds', 'last2', False),
    'staff_no':    ('n10', r'Administrative and project management', 'staff', False),
    'salaries':    ('n10', r'Salaries and wages', 'last2', False),
    'nic':         ('n10', r'Social security costs', 'last2', False),
    'pension':     ('n10', r'Other pension costs', 'last2', False),
    'capex':       ('n11', r'Additions', 'one', False),
}
# the lines of note 5, "Analysis of expenditure", in the order of the report
SPEND = {
    'sp_staff': r'Staff costs', 'sp_food': r'Welfare & food', 'sp_maint': r'Maintenance',
    'sp_depr': r'Depreciation', 'sp_heat': r'Heat, light', 'sp_ins': r'Insurance', 'sp_travel': r'Travel',
    'sp_pubs': r'Publications', 'sp_print': r'Printing & postage', 'sp_legal': r'Legal and professional',
    'sp_comms': r'Communications', 'sp_don': r'Donations', 'sp_bank': r'Bank Charges',
    'sp_equip': r'Sundry capital equipment', 'sp_admin': r'Other administration', 'sp_gov': r'Governance costs',
}
for k, lab in SPEND.items():
    ITEMS[k] = ('n5', lab, 'last2', False)


def number(tok):
    """'1,234' -> 1234, '(1,234)' -> -1234, '-' -> 0; None if it can't be read safely."""
    if tok in ('-', '–'):
        return 0
    if not tok:
        return None
    neg = tok[0] in '({-' or tok[-1] in ')}'
    t = tok.strip('(){}-')
    t = t.translate(str.maketrans({'l': '1', 'L': '1', 'I': '1', 'O': '0', 'o': '0', 'S': '8'}))
    if not re.fullmatch(r'\d{1,3}(,\d{3})*|\d{1,3}', t):
        return None
    return -int(t.replace(',', '')) if neg else int(t.replace(',', ''))


def numbers(rest):
    rest = re.sub(r'(\d),\s+(\d{3})\b', r'\1,\2', rest)            # "1,045, 794" -> "1,045,794"
    out = []
    for tok in rest.split():
        if re.search(r'\d', tok) or tok in ('-', '–'):
            out.append(number(tok))
        elif out:
            break                                                  # words after the numbers
    return out


def loose(pattern):
    """Let a space in a pattern match any run of spaces: scanned pages are spaced out unevenly."""
    return pattern.replace(' ', r'\s+')


def section(text, name):
    start, end = (loose(x) for x in SECTIONS[name])
    lines = text.splitlines()
    i = next((n for n, l in enumerate(lines) if re.search(start, l.strip())), None)
    if i is None:
        return lines                                               # heading lost in a scan: search the whole report
    j = next((n for n in range(i + 1, len(lines)) if re.search(end, lines[n].strip())), len(lines))
    return lines[i:j]


def read(year):
    text = (here / 'txt' / f'{year}.txt').read_text(encoding='utf-8')
    cur, prev, notes = {}, {}, []
    for key, (sec, label, how, optional) in ITEMS.items():
        label = loose(label)
        line = next((l for l in section(text, sec) if re.match(r'\s*' + label + r'\b', l)), None)
        if line is None:
            if not optional:
                notes.append(f'{key}: line "{label}" not found')
            continue
        rest = re.sub(r'^\s*' + label, '', line)
        ns = numbers(rest)
        lines_ = section(text, sec)
        at = lines_.index(line)
        for extra in lines_[at + 1:at + 3]:                        # a label over two lines: "TOTAL INCOMING / RESOURCES  1,234 ..."
            if how != 'last2' or len([n for n in ns if n is not None]) >= 2:
                break
            ns = numbers(re.sub(r'^\s*[A-Za-z][A-Za-z ,()/]*?(?=\s{2,}|$)', '', extra))
        if how == 'last2' and ns and abs(ns[0] or 0) < 30 and len(ns) >= 3:
            ns = ns[1:]                                            # a note number such as "13"
        if how == 'last2' and len(ns) >= 2:
            cur[key], prev[key] = ns[-2], ns[-1]
        elif how == 'note2' and len(ns) in (6, 4):
            cur[key], prev[key] = (ns[2], ns[5]) if len(ns) == 6 else (ns[1], ns[3])
        elif how == 'staff' and len(ns) == 4:
            cur[key], prev[key] = ns[0], ns[2]
        elif how == 'unr6' and len(ns) == 6:
            cur[key], prev[key] = ns[0], ns[3]
        elif how == 'one' and ns:
            cur[key] = ns[-1]
        else:
            notes.append(f'{key}: could not read "{line.strip()}"')
    # the general fund: the money free for day-to-day running. Note "Funds movement" has a row
    # "General funds  start  income  (spending)  transfers  end" for the group, the company, then the same for last year.
    rows = [numbers(re.sub(r'^\s*General\s+funds', '', l)) for l in section(text, 'n15') if re.match(r'\s*General\s+funds\b', l)]
    rows = [r for r in rows if len(r) == 5 and None not in r]
    if len(rows) == 4:
        for d, r in ((cur, rows[0]), (prev, rows[2])):
            d['gen_in'], d['gen_out'], d['gen_moved'] = r[1], -r[2], r[3]
    else:
        notes.append('general fund rows not read')
    m = re.search(r'(\S+)\s+retained\s+as', text)                 # the reserves the trustees aim for
    if m:
        cur['target'] = number(re.sub(r'^[^\d]+', '', m.group(1)))
    # gifts from one donor, named in the trustees' financial review: "donations totalling £625,000 (2022-23: £625,000) from one donor"
    flat = ' '.join(text.split())
    m = re.search(r'donations totall?ing (\S+(?: \d{3})?) (?:\((?:\d{4}-\d\d:? )?(\S+?)\) )?from one donor', flat)
    if m:
        money = lambda t: number(re.sub(r'^[^\d]+', '', t.replace(', ', ',')))
        cur['one_donor'] = money(m.group(1))
        if m.group(2):
            prev['one_donor'] = money(m.group(2))
    for d in (cur, prev):
        for k in [k for k, v in d.items() if v is None]:
            notes.append(f'{k}: unreadable number')
            del d[k]
    return cur, prev, notes


def main():
    reports = sorted(int(p.stem) for p in (here / 'txt').glob('*.txt'))
    got = {y: read(y) for y in reports}
    years = list(range(reports[0] - 1, reports[-1] + 1))
    corrections = {}
    cf = here / 'corrections.txt'
    if cf.exists():
        for line in cf.read_text(encoding='utf-8').splitlines():
            line = line.split('#')[0].strip()
            if line:
                y, k, v = line.split()
                corrections[(int(y), k)] = number(v)

    hand = {}                                      # read_by_hand.txt: the years before DETAIL_FROM, read by eye from the scans
    for line in (here / 'read_by_hand.txt').read_text(encoding='utf-8').splitlines():
        line = line.split('#')[0].strip()
        if line:
            y, k, v = line.split()
            hand.setdefault(int(y), {})[k] = number(v)

    data, source, differ = {}, {}, []
    for y in years:
        if y < DETAIL_FROM:
            data[y] = dict(hand.get(y, {}))
            data[y].setdefault('gains', 0)
            data[y].setdefault('other', 0)
            source[y] = {k: 'read_by_hand.txt' for k in data[y]}
            continue
        own = got.get(y, ({}, {}, []))[0]
        nxt = got.get(y + 1, ({}, {}, []))[1]
        first, second = (nxt, own) if y in SCANNED else (own, nxt)
        row, src = {}, {}
        for k in list(ITEMS) + ['target', 'one_donor', 'gen_in', 'gen_out', 'gen_moved', 'restricted_in']:
            if (y, k) in corrections:
                row[k], src[k] = corrections[(y, k)], 'corrections.txt'
            elif k in first:
                row[k], src[k] = first[k], f'{y + 1 if first is nxt else y} report'
            elif k in second:
                row[k], src[k] = second[k], f'{y + 1 if second is nxt else y} report'
            if k in own and k in nxt and abs(own[k] - nxt[k]) > 2 and (y, k) not in corrections:
                differ.append(f'{y} {k}: {own[k]:,} in the {y} report, {nxt[k]:,} in the {y + 1} report; using {row[k]:,}')
        row.setdefault('gains', 0)
        row.setdefault('investments', 0)
        data[y], source[y] = row, src

    problems = []   # a line one report can't give is only a problem when no other copy has the figure (see "no figure for")

    def check(y, what, a, b, tol=2):
        if a is None or b is None:
            if y >= DETAIL_FROM:
                problems.append(f'{y}: cannot check {what} (figure missing)')
        elif abs(a - b) > tol:
            problems.append(f'{y}: {what}: {a:,} vs {b:,} (off by {a - b:,})')

    g = lambda y, k: data.get(y, {}).get(k)
    for y in years:
        r = data[y]
        s = lambda *ks: None if any(k not in r for k in ks) else sum(r[k] for k in ks)
        check(y, 'donations + interest + other = income', s('donations', 'interest', 'other'), r.get('income'))
        check(y, 'gifts + legacies = donations', s('gifts', 'legacies'), r.get('donations'))
        if y >= DETAIL_FROM:
            check(y, 'spending lines = total spending', s(*SPEND), r.get('spending'))
        check(y, 'income - spending + gains = net income', s('income', 'gains') - r['spending'] if 'spending' in r and s('income', 'gains') is not None else None, r.get('net'))
        if y >= DETAIL_FROM:
          check(y, 'what it owns less what it owes = net assets', s('buildings', 'investments', 'debtors', 'cash', 'creditors'), r.get('net_assets'))
          check(y, 'net assets = funds', r.get('net_assets'), r.get('funds'))
        if y >= DETAIL_FROM:
            check(y, 'restricted + designated + general + £12 shares = funds', (s('restricted', 'designated', 'general') or 0) + 12, r.get('funds'))
        if 'restricted_in' in r:
            check(y, 'income for a set purpose no more than all income', min(r['restricted_in'], r['income']), r['restricted_in'])
        check(y, 'unrestricted gifts no more than all gifts', min(r.get('gifts_u', 0), r.get('gifts', 0)), r.get('gifts_u'))
        if y - 1 in data:
            start = r.get('gen_start', g(y - 1, 'general'))
            if 'gen_in' in r and start is not None:
                check(y, "general fund at the start + in - out + moved + gains = general fund", start + r['gen_in'] - r['gen_out'] + r['gen_moved'] + r.get('gen_gain', 0), r.get('general'))
        if y < DETAIL_FROM and 'general' in r and 'designated' in r and 'restricted' in r:
            check(y, 'restricted + designated + general + £12 shares = funds', r['restricted'] + r['designated'] + r['general'] + 12, r.get('funds'), tol=15)
            check(y, "last year's funds + net income = funds", None if None in (g(y - 1, 'funds'), r.get('net')) else g(y - 1, 'funds') + r['net'], r.get('funds'))
            parts = [g(y - 1, 'buildings'), r.get('capex'), r.get('sp_depr')]
            if r.get('capex') is not None:
                check(y, "buildings last year + building spending - depreciation = buildings",
                      None if None in parts else parts[0] + parts[1] - parts[2], r.get('buildings'), tol=5000)
        for k in ITEMS:
            if y < DETAIL_FROM and k not in CORE:
                continue
            if k not in r and not ITEMS[k][3] and not (k == 'capex' and y == years[0]):
                problems.append(f'{y}: no figure for {k}')

    json.dump({'years': years, 'data': {str(y): data[y] for y in years}, 'source': {str(y): source[y] for y in years}},
              open(here / 'data.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(f'{len(years)} years ({years[0]}–{years[-1]}) from {len(reports)} reports -> data.json')
    if differ:
        print('\nThe two copies of a figure differ (usually a misread digit in a scan):')
        print('\n'.join('  ' + d for d in differ))
    print('\nChecks:', 'all add up.' if not problems else f'{len(problems)} problem(s)')
    print('\n'.join('  ' + p for p in problems))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
