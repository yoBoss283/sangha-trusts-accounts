# Builds data.json (euros, calendar years 2013-2025) from the two pages of the abbots' report (report.pdf):
#   expenses.json  (page 1, read by extract_report.py: every line of expense per year, with the report's own totals)
#   raw_balance.json (page 2: balance sheet)
# Checks that the lines add up to the report's totals and prints every difference (the owner's sheet has three).
import json, pathlib
here = pathlib.Path(__file__).parent
raw = json.load(open(here / 'raw_expenses.json'))
rows = []                                   # rows with the same label next to each other are one line (its colours sit at different heights)
for l, d in raw:
    if rows and rows[-1][0] == l and not (set(rows[-1][1]) & set(d)): rows[-1][1].update(d)
    else: rows.append([l, dict(d)])
# 2012-2024: the community's accounts spreadsheet (read_spreadsheet.py); 2025: the two-page report (the spreadsheet stops at 2024)
sheet = json.load(open(here / 'spreadsheet.json'))
for rr, (label, d) in sheet['rows'].items():
    row_ = rows[int(rr)][1]
    for y in [y for y in row_ if int(y) <= 2024]: del row_[y]
    row_.update(d)
rows[15][1]['2015'] = sheet['clearing_land_2015']          # footnote (a): missing from the spreadsheet's main sheet
bal = {l or str(i): d for i, (l, d) in enumerate(json.load(open(here / 'raw_balance.json')))}
def row(i): return rows[i][1]
G = {   # row numbers in expenses.json -> kind
 'util':      [22, 23, 24, 25],            # electricity, water, gas, wood
 'upkeep':    [33],                        # repairs and maintenance of the house
 'insurance': [31, 32],                    # insurance, fire extinguishers and safety
 'rent':      [26],
 'travel':    [29, 30, 34, 35, 36],        # car fuel, car tax and upkeep, travel, stays
 'welfare':   [37, 39, 40, 41],            # health, clothes, food, vet
}
PROJECT = [7, 8, 9, 10, 11, 15, 16, 18, 43]   # building project: survey, architects, engineers, legal for the project,
                                               # shelters, clearing land, tools for the project, tax on land
WRITEOFF = [45, 46]      # depreciation entered on its own line (2017), loss on fixed assets (write-offs, not money paid)
tot, run_given, dep = row(48), row(49), row(47)
out = {}
issues = []
for y in map(str, range(2013, 2026)):
    g = lambda ids: round(sum(row(i).get(y, 0) for i in ids), 2)
    r = {'spending': tot[y], 'depr': dep.get(y, 0), 'writeoff': g(WRITEOFF), 'project': g(PROJECT), 'interest': -g([13])}
    for k, ids in G.items(): r[k] = g(ids)
    lines = round(sum(v.get(y, 0) for i, v in enumerate(r_[1] for r_ in rows) if i not in (0, 48, 49)), 2)
    if abs(lines - tot[y]) > 0.05: issues.append((y, round(tot[y] - lines, 2)))
    assert abs(tot[y] - dep.get(y, 0) - run_given[y]) < 0.05, y
    out[y] = r
# the balance sheet
def b(key, y):
    for l, d in bal.items():
        if l.startswith(key) and y in d: return d[y]
fa = {y: (b('Activos fixos', y) or 0) + (b('Projectos em Curso', y) or 0) for y in map(str, range(2012, 2026))}
eq = {y: b('Total do capital', y) for y in map(str, range(2012, 2026))}
# two balance-sheet slips in the spreadsheet, worked out from the rest of the balance sheet (footnotes d and e)
fa['2021'] = 2527052.89      # the posted total of fixed assets and work in progress; its two lines add up to 4,000 less
eq['2012'] = 71871.16        # assets less liabilities; the posted 27,347.60 is 44,523.56 too low
for y in map(str, range(2013, 2026)):
    r = out[y]
    r['buildings'] = round(fa[y], 2)
    r['capex'] = round(fa[y] - fa[str(int(y) - 1)] + r['depr'], 2)     # additions: change in what is owned, plus the wear written off
    r['equity'] = eq[y]
    r['result'] = b('Resultado l', y) if b('Resultado l', y) is not None and y == '2013' else round(eq[y] - eq[str(int(y) - 1)], 2)   # 2012's equity line in the report does not match its own assets, so 2013 takes the reported result
    r['cash'] = round((b('Caixa e dep', y) or 0), 2)
    r['deposits'] = round((b('Outros activos financeiros', y) or 0), 2)
    r['income'] = round(r['result'] + r['spending'], 2)                  # worked out: result + spending (the report has no income line)
json.dump(out, open(here / 'data.json', 'w'), indent=1)
print('differences between the sum of the lines and the report total:', issues)
for y, r in out.items():
    run = r['spending'] - r['depr'] - r['writeoff'] - r['project'] + r['interest']
    print(y, 'run', round(run), 'util', round(r['util']), 'upkeep', round(r['upkeep']), 'ins', round(r['insurance']), 'rent', round(r['rent']), 'trav', round(r['travel']), 'welf', round(r['welfare']), '| proj', round(r['project']), 'capex', round(r['capex']), 'income', round(r['income']), 'cash', round(r['cash'] + r['deposits']))

# footnotes: every place where the page uses a different number from the one posted in the spreadsheet
NOTES = [
 {'id': 'a', 'marks': [['Total expenses in the report', '2015'], ['less building-project costs listed as expenses', '2015']],
  'text': "2015: the spreadsheet's main sheet leaves out the line Clearing land (€6,360.00), which its separate 2015 sheet has. With it, the lines add up to the posted total of €122,606.05; without it they are €6,360 short. The page counts it as building-project costs."},
 {'id': 'b', 'marks': [['Total expenses in the report', '2017']],
  'text': "2017: the lines add up to €3.80 less than the posted total (€40,573.83). The page uses the posted total; the €3.80 is in \"Office, fees and the rest\"."},
 {'id': 'c', 'marks': [['Total expenses in the report', '2022'], ['Total expenses in the report', '2023']],
  'text': "2022 and 2023: the totals are as posted in the spreadsheet (€44,445.17 and €144,112.04), and its lines add up to them. The earlier two-page report gave €44,371.91 and €144,040.36, which is the bank charges (€73.26 and €71.68) less."},
 {'id': 'd', 'marks': [['Land, buildings and work in progress, 31 Dec', '2021'], ['New buildings and infrastructure', '2021'], ['New buildings and infrastructure', '2022']],
  'text': "2021: the posted total of fixed assets and work in progress is €2,527,052.89. The two lines above it add up to €4,000 less (€2,523,052.89). The page uses the total, because only it matches total assets, liabilities and equity. So new buildings are €4,000 more in 2021 and €4,000 less in 2022 than the lines would give."},
 {'id': 'e', 'marks': [['Money given, worked out (result + expenses)', '2013']],
  'text': "2012 equity: the spreadsheet posts €27,347.60, but total assets are €71,871.16 and there are no liabilities, so the page uses €71,871.16. That makes the 2013 result €113,029.67, as the spreadsheet itself reports for 2013 (the posted figures would give €157,553.23)."},
 {'id': 'f', 'marks': [['Total expenses in the report', '2025']],
  'text': "2025: the spreadsheet stops at 2024, so 2025 is from the community's two-page report to the abbots. Its lines add up to €120.93 less than its total, and the report enters interest received (€1,453.74) as a negative cost."},
]
json.dump(NOTES, open(here / 'footnotes.json', 'w'), indent=1, ensure_ascii=False)
