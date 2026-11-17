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
