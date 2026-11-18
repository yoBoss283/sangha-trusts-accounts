# Build the landing page index.html for the accounts pages in the folders next to it (est/, aruna-ratanagiri/, hartridge/, sumedharama/),
# and copy the detail pages into pages/
# with a "back to all three" link on top. The figures come from each page's own data (last three years, as paid), so the
# cards agree with the detail pages. Run: python3 build.py   (after rebuilding the three detail pages with their build.py)
import json, pathlib, datetime, re
here = pathlib.Path(__file__).parent
docs = here.parent
A = {'est': here / 'est', 'ratanagiri': here / 'aruna-ratanagiri', 'hartridge': here / 'hartridge', 'sumedharama': here / 'sumedharama'}
FILES = {'est': 'est-accounts.html', 'ratanagiri': 'ratanagiri-accounts.html', 'hartridge': 'hartridge-accounts.html', 'sumedharama': 'sumedharama-accounts.html'}

def load(k):
    d = json.load(open(A[k] / 'data.json')); p = json.load(open(A[k] / 'people.json'))
    return (d['data'] if k == 'est' else d), p
g = lambda r, k: r.get(k) or 0
RUN = {'est': lambda r: r['spending'] - g(r, 'sp_depr') - g(r, 'x_plan') - g(r, 'x_loan') - g(r, 'x_temple'),
       'ratanagiri': lambda r: r['spending'] - g(r, 'depr') - g(r, 'disposal'),
       'hartridge': lambda r: r['spending'] - g(r, 'capfund'),
       'sumedharama': lambda r: r['spending'] - g(r, 'depr') - g(r, 'writeoff') - g(r, 'project') + g(r, 'interest')}
fig = {}
for k in A:
    D, P = load(k)
    ys = sorted(int(y) for y in D)[-3:]
    year = sum(RUN[k](D[str(y)]) for y in ys) / 3
    fig[k] = {'years': f'{ys[0]}–{str(ys[-1])[2:]}', 'year': year, 'day': year / 365,
              'people': sum(P[str(y)]['people'] for y in ys) / 3, 'last': (ys[-1], P[str(ys[-1])]['people'])}

# ---- the numbers typed in the card sentences are computed here, from the same data the pages use
def real(D, C, run, ys, base_year):                  # average a year of the years `ys`, in `base_year` prices
    return sum(run(D[str(y)]) * C[str(base_year)] / C[str(y)] for y in ys) / len(ys)
def data(k):
    return json.load(open(A[k] / 'data.json')), json.load(open(A[k] / 'cpi.json'))
facts = {}
D, C = data('est'); D = D['data']
runw = lambda r: RUN['est'](r) - g(r, 'sp_food')                                     # without welfare and food
b, n = real(D, C, runw, [2016, 2017, 2018], 2026), real(D, C, runw, [2024, 2025, 2026], 2026)
facts['est_rise'], facts['est_pct'] = round((n - b) / 1000) * 1000, round(100 * (n / b - 1))
assert D['2019'].get('capex') is None, 'EST 2019 now has capex: update the £3.0m rule'
facts['est_build'] = sum(g(D[str(y)], 'capex') for y in range(2019, 2027) if y != 2019) + 3.0e6   # as the EST page: £3.0m in 2019 + later capex
D, C = data('ratanagiri')
b1, b2, b3 = (real(D, C, RUN['ratanagiri'], range(a, a + 5), 2025) for a in (2011, 2016, 2021))
assert abs(b2 / b1 - 1) < 0.03, 'Ratanagiri 2016-20 is no longer level with 2011-15'
facts['rat_pct'] = round(100 * (b3 / b2 - 1))
fixed = lambda r: g(r, 'heat') + g(r, 'repairs') + g(r, 'rent') + g(r, 'ins')
facts['rat_fixed'] = round(100 * sum(fixed(D[str(y)]) for y in range(2021, 2026)) / sum(RUN['ratanagiri'](D[str(y)]) for y in range(2021, 2026)))
D, C = data('hartridge'); P = json.load(open(A['hartridge'] / 'people.json'))
h1, h3 = real(D, C, RUN['hartridge'], range(2013, 2016), 2025), real(D, C, RUN['hartridge'], range(2021, 2026), 2025)
facts['hart_pct'] = round(100 * (h3 / h1 - 1))
facts['hart_fixed'] = round(100 * sum(g(D[str(y)], 'utilities') + g(D[str(y)], 'estate') for y in range(2023, 2026)) / sum(RUN['hartridge'](D[str(y)]) for y in range(2023, 2026)))
p1 = sum(P[str(y)]['people'] for y in range(2013, 2016)) / 3; p3 = sum(P[str(y)]['people'] for y in range(2021, 2026)) / 5
assert p3 >= 2 * p1, 'Hartridge community has no longer doubled'
facts['hart_p'] = (round(p1), round(p3))
def since(k, base, now, py, run):                    # 2019-21 against the latest three years, after inflation, with welfare and food
    D, C = data(k); D = D['data'] if k == 'est' else D
    f = lambda ys: real(D, C, run, ys, py)
    a, b = f(base), f(now)
    return round(100 * (b / a - 1)), round((b - a) / 1000) * 1000
facts['est_since'] = since('est', [2019, 2020, 2021], [2024, 2025, 2026], 2026, RUN['est'])
facts['rat_since'] = since('ratanagiri', [2019, 2020, 2021], [2023, 2024, 2025], 2025, RUN['ratanagiri'])
facts['hart_since'] = since('hartridge', [2019, 2020, 2021], [2023, 2024, 2025], 2025, RUN['hartridge'])
facts['rat_build'] = sum(g(json.load(open(A['ratanagiri'] / 'data.json'))[str(y)], 'capex') for y in range(2011, 2026))
facts['hart_build'] = sum(g(json.load(open(A['hartridge'] / 'data.json'))[str(y)], 'capex') for y in range(2013, 2026))
D, C = data('sumedharama'); P = json.load(open(A['sumedharama'] / 'people.json'))
s1, s3 = real(D, C, RUN['sumedharama'], range(2013, 2016), 2025), real(D, C, RUN['sumedharama'], range(2021, 2026), 2025)
norent = lambda r: RUN['sumedharama'](r) - g(r, 'rent')
facts['sum_pct'] = round(100 * (s3 / s1 - 1))
facts['sum_pct_norent'] = round(100 * (real(D, C, norent, range(2021, 2026), 2025) / real(D, C, norent, range(2013, 2016), 2025) - 1))
half = lambda x: f'{round(x * 2) / 2:g}'
facts['sum_p'] = (half(sum(P[str(y)]['people'] for y in range(2013, 2016)) / 3), half(sum(P[str(y)]['people'] for y in range(2021, 2026)) / 5))
facts['sum_since'] = since('sumedharama', [2019, 2020, 2021], [2023, 2024, 2025], 2025, RUN['sumedharama'])
print(facts)
CUR = {'sumedharama': '€'}
r1000 = lambda n, k='': f'{CUR.get(k, "£")}{round(n / 1000) * 1000:,}'
r5 = lambda n, k='': f'{CUR.get(k, "£")}{round(n / 5) * 5:,}'
CARDS = [
 ('est', 'Amaravati and Chithurst', 'English Sangha Trust · Hertfordshire and West Sussex · two monasteries', '--s1',
  f'Without welfare and food, running costs went from about £{round(b, -4):,.0f} to about £{round(n, -4):,.0f} a year in 2026 money (+£{facts["est_rise"]:,}, {facts["est_pct"]}% more).'),
 ('ratanagiri', 'Aruna Ratanagiri', 'Harnham Buddhist Monastery Trust · Harnham, Northumberland', '--s2',
  f'After inflation, running costs were level from 2011–15 to 2016–20, then rose {facts["rat_pct"]}% in 2021–25. Heat and light followed energy prices; about {facts["rat_fixed"]}% of the costs (heat, repairs, rent, rates and insurance, 2021–25) come with the buildings.'),
 ('hartridge', 'Hartridge', 'Hartridge Buddhist Monastery Trust · Upottery, Devon', '--s3',
  f'After inflation, running costs in 2021–25 were {facts["hart_pct"]}% higher than in 2013–15, while the community more than doubled ({facts["hart_p"][0]} in 2013–15, {facts["hart_p"][1]} in 2021–25). Rates, utilities and the grounds are {facts["hart_fixed"]}% of the cost.'),
 ('sumedharama', 'Sumedharama', 'Budismo Theravada da Floresta · Portugal · amounts in euros', '--s4',
  f'After inflation, and leaving out the rent paid until 2018, running costs in 2021–25 were {facts["sum_pct_norent"]}% higher than in 2013–15; counting that rent, {abs(facts["sum_pct"])}% {"lower" if facts["sum_pct"] < 0 else "higher"}. The community more than doubled ({facts["sum_p"][0]} to {facts["sum_p"][1]}). The source is the community\'s own accounts spreadsheet, not filed accounts.'),
]
def signed(n, unit=''):
    return ('+' if n >= 0 else '−') + unit + f'{abs(n):,}'
SINCE = {k: facts[k + '_since'] for k in ('est', 'rat', 'hart')}
SINCE = {'est': SINCE['est'], 'ratanagiri': SINCE['rat'], 'hartridge': SINCE['hart'], 'sumedharama': facts['sum_since']}
BUILD = {'est': ('2019–26', f'£{facts["est_build"] / 1e6:.1f} million'),
         'ratanagiri': ('2011–25', f'£{round(facts["rat_build"], -3):,}'),
         'hartridge': ('2013–25', f'£{round(facts["hart_build"], -3):,}')}
EXTRA = {'est': 'including welfare and food, ', 'ratanagiri': '', 'hartridge': '', 'sumedharama': ''}
cards = ''
for k, name, where, col, says in CARDS:
    f = fig[k]
    cards += f'''<article class="place"><div class="bar" style="background:var({col})"></div>
  <h2>{name}</h2><p class="where">{where}</p>
  <p class="big">{r1000(f["year"], k)}</p><p class="bigl">a year to run, {EXTRA[k]}without building work and one-off building costs, as paid, {f["years"]} average</p>
  <dl><dt>A day ({f["years"]} average)</dt><dd>{r5(f["day"], k)}</dd><dt>A day for each resident<span style="display:block;font-size:12.5px;opacity:.75">{round(f["people"])} on average</span></dt><dd>{CUR.get(k, "£")}{round(f["day"] / f["people"])}</dd><dt>A year for each resident</dt><dd>{CUR.get(k, "£")}{round(f["year"] / f["people"], -2):,.0f}</dd></dl>
  <p class="says">{says}</p>
  <p class="since"><b>Since 2019–21, after inflation:</b> <span style="white-space:nowrap">{signed(SINCE[k][0])}%</span> <span style="white-space:nowrap">({signed(SINCE[k][1], CUR.get(k, "£")) + " a year" if SINCE[k][1] else "about the same each year"})</span>, {"with welfare and food" if k == "est" else "all running costs"}</p>
  <a class="go" href="pages/{k}.html">Read the full report →</a></article>
'''
# earlier copies of the site (made with archive.py before an update), newest first; the markers let archive.py leave this out of a copy
_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
_old = sorted((d.name for d in (here / 'archive').glob('*') if d.is_dir() and (d / 'index.html').exists()), reverse=True)
EARLIER = ('<!--earlier--><b>Earlier versions:</b> ' + ', '.join(f'<a href="archive/{n}/index.html">{_months[int(n[5:7]) - 1]} {n[:4]}</a>' for n in _old) + '. <!--/earlier-->') if _old else ''
body = f'''
<main id="top">
<header>
  <p class="kicker">Accounts of the monasteries, from their published annual reports</p>
  <h1>What it costs to run the monasteries</h1>
  <p class="hero">Five monasteries: Amaravati and Chithurst (one trust), Aruna Ratanagiri, Hartridge and Sumedharama in Portugal. Each report below says, in plain words, what the place costs to run, what the money goes on, and how that has changed after inflation.</p>
</header>
<section class="story">
  <div class="places">
{cards}  </div>
  <div class="card" style="margin-top:16px"><h3>How to read these side by side</h3>
    <p class="note">Not a ranking: the places are different sizes and the amounts are as paid at the time, averaged over each place's last three years. Sumedharama's accounts are in euros, so its amounts are in euros, not converted.</p>
    <p class="note"><b>One measure the same for all:</b> running costs after inflation, the three years 2019–21 against each place's last three years. The English Sangha Trust {signed(SINCE["est"][0])}%, Aruna Ratanagiri {signed(SINCE["ratanagiri"][0])}%, Hartridge {signed(SINCE["hartridge"][0])}%, Sumedharama {signed(SINCE["sumedharama"][0])}% (compared in its own euros and Portuguese prices). The places differ in size, in how many people live there and in building work, so this shows how each changed, not which is better run.</p>
    <details class="how"><summary>More about the figures</summary>
    <p class="note">Amaravati and Chithurst are two monasteries run together: the accounts do not give a figure for each. A day (or a year) for each resident is the cost of a day (or a year) divided by the number of residents (the monks, nuns, novices and anagārikas living there). It is a simple guide: guests, retreatants and visitors use the place too, so it is not what one person costs.</p>
    <p class="note"><b>Running costs</b> means everything the trust spends in a year to keep the place going, without new buildings and without wear on buildings (depreciation, which is not money paid out). Each report also takes out a few building costs the accounts count as spending; the notes in each report list them. The English Sangha Trust's own page quotes its latest year (£2,770 a day in the year to March 2026).</p>
    <p class="note"><b>Years.</b> The English Sangha Trust's year runs from April to March (2024–26 is the years to March 2024, 2025 and 2026). The others run January to December. <b>Residents</b> are averaged over the same years.</p></details>
  </div>
  <p class="sources"><b>Sources anyone can check:</b> the trusts' annual reports on the Charity Commission register and at Companies House: <a href="https://find-and-update.company-information.service.gov.uk/company/00565499/filing-history?category=accounts" target="_blank" rel="noopener">English Sangha Trust</a> (charity 231310), <a href="https://find-and-update.company-information.service.gov.uk/company/06688355/filing-history?category=accounts" target="_blank" rel="noopener">Harnham Buddhist Monastery Trust</a> (charity 1126476), <a href="https://find-and-update.company-information.service.gov.uk/company/07387479/filing-history?category=accounts" target="_blank" rel="noopener">Hartridge Buddhist Monastery Trust</a> (charity 1142439). Sumedharama: the community's own accounts spreadsheet (expenses and balance sheet, 2012–2024) and, for 2025, its two-page report to the abbots, shared by Ajahn Vajiro; they are not filed accounts. <b>Made by</b> Narindo. <b>Code and data:</b> <a href="https://github.com/yoBoss283/sangha-trusts-accounts" target="_blank" rel="noopener">github.com/yoBoss283/sangha-trusts-accounts</a>. {EARLIER}<span class="tag">Updated {datetime.datetime.now(datetime.timezone.utc).strftime("%-d %B %Y, %H:%M GMT")}</span></p>
</section>
</main>
'''
full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + (here / 'head.tmp').read_text().replace('</style>', '</style>\n</head>\n<body>', 1) + body + '\n</body>\n</html>\n')
(here / 'index.html').write_text(full, encoding='utf-8')
back = '<p class="back"><a href="../index.html">← All the monasteries</a></p>'
for k, f in FILES.items():
    h = (A[k] / f).read_text(encoding='utf-8')
    assert '<main id="top">' in h, k
    page = h.replace('<main id="top">', '<main id="top">\n' + back, 1)
    (here / 'pages' / f'{k}.html').write_text(page, encoding='utf-8')      # the address people already have
    (A[k] / 'index.html').write_text(page, encoding='utf-8')                # the same page at /<folder>/
for k in fig:
    print(k, fig[k]['years'], r1000(fig[k]['year']), r5(fig[k]['day']), round(fig[k]['people']))
print('wrote index.html and pages/')
