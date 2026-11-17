# Build the landing page index.html for the three trusts' accounts pages, and copy the three detail pages into pages/
# with a "back to all three" link on top. The figures come from each page's own data (last three years, as paid), so the
# cards agree with the detail pages. Run: python3 build.py   (after rebuilding the three detail pages with their build.py)
import json, pathlib, datetime, re
here = pathlib.Path(__file__).parent
docs = here.parent
A = {'est': docs / 'Sangha accounts statistics', 'ratanagiri': docs / 'Aruna Ratanagiri accounts statistics', 'hartridge': docs / 'Hartridge accounts statistics'}
FILES = {'est': 'est-accounts.html', 'ratanagiri': 'ratanagiri-accounts.html', 'hartridge': 'hartridge-accounts.html'}

def load(k):
    d = json.load(open(A[k] / 'data.json')); p = json.load(open(A[k] / 'people.json'))
    return (d['data'] if k == 'est' else d), p
g = lambda r, k: r.get(k) or 0
RUN = {'est': lambda r: r['spending'] - g(r, 'sp_depr') - g(r, 'x_plan') - g(r, 'x_loan') - g(r, 'x_temple'),
       'ratanagiri': lambda r: r['spending'] - g(r, 'depr') - g(r, 'disposal'),
       'hartridge': lambda r: r['spending'] - g(r, 'capfund')}
fig = {}
for k in A:
    D, P = load(k)
    ys = sorted(int(y) for y in D)[-3:]
    year = sum(RUN[k](D[str(y)]) for y in ys) / 3
    fig[k] = {'years': f'{ys[0]}–{str(ys[-1])[2:]}', 'year': year, 'day': year / 365,
              'people': sum(P[str(y)]['people'] for y in ys) / 3}
r1000 = lambda n: f'£{round(n / 1000) * 1000:,}'
r5 = lambda n: f'£{round(n / 5) * 5:,}'
CARDS = [
 ('est', 'Amaravati and Chithurst', 'English Sangha Trust · Hertfordshire and West Sussex · two monasteries', '--s1',
  'Since 2016–18, running costs (without welfare) have risen by £141,000 a year, 22% more, after inflation. In the same years the trust also spent £20.5 million on new buildings, which is not counted in running costs.'),
 ('ratanagiri', 'Aruna Ratanagiri', 'Harnham Buddhist Monastery Trust · Harnham, Northumberland', '--s2',
  'After inflation, running costs were level from 2011–15 to 2016–20, then rose 11% in 2021–25. Heat and light followed energy prices; about 45% of the costs come with the buildings.'),
 ('hartridge', 'Hartridge', 'Hartridge Buddhist Monastery Trust · Upottery, Devon', '--s3',
  'After inflation, running costs are 19% higher than in 2013–15, while the community more than doubled, from 3 to 7. Rates, utilities and the grounds are 59% of the cost.'),
]
cards = ''
for k, name, where, col, says in CARDS:
    f = fig[k]
    cards += f'''<article class="place"><div class="bar" style="background:var({col})"></div>
  <h2>{name}</h2><p class="where">{where}</p>
  <p class="big">{r1000(f["year"])}</p><p class="bigl">a year to run, {f["years"]} average</p>
  <dl><dt>A day</dt><dd>{r5(f["day"])}</dd><dt>A day for each resident ({round(f["people"])} residents)</dt><dd>£{round(f["day"] / f["people"])}</dd></dl>
  <p class="says">{says}</p>
  <a class="go" href="pages/{k}.html">Read the full report →</a></article>
'''
body = f'''
<main id="top">
<header>
  <p class="kicker">Accounts of the monasteries, from their published annual reports</p>
  <h1>What it costs to run the monasteries</h1>
  <p class="hero">Four monasteries, looked after by three charitable trusts. Each report below says, in plain words, what the place costs to run, what the money goes on, and how that has changed after inflation.</p>
</header>
<section class="story">
  <div class="places">
{cards}  </div>
  <div class="card" style="margin-top:16px"><h3>How to read these side by side</h3>
    <p class="note">The places are not the same size, and Amaravati and Chithurst are two monasteries run together: the accounts do not give a figure for each. So the cards show what each trust spends, not a ranking. A day for each resident is the cost of a day divided by the number of residents (the monks, nuns, novices and anagārikas living there). It is a simple guide: guests, retreatants and visitors use the place too, so it is not what one person costs.</p>
    <p class="note"><b>Running costs</b> means everything the trust spends in a year to keep the place going, without new buildings and without wear on buildings (depreciation, which is not money paid out). Each report also takes out a few building costs the accounts count as spending; the notes in each report list them. Amounts are as paid at the time, averaged over each trust's last three years. The English Sangha Trust's own page quotes its latest year (£2,770 a day in the year to March 2026).</p>
    <p class="note"><b>Years.</b> The English Sangha Trust's year runs from April to March (2024–26 is the years to March 2024, 2025 and 2026). The other two run January to December. <b>Residents</b> are the monks, nuns, novices and anagārikas on the community lists, averaged over the same years.</p>
  </div>
  <p class="sources"><b>Sources anyone can check:</b> the trusts' annual reports on the Charity Commission register and at Companies House: <a href="https://find-and-update.company-information.service.gov.uk/company/00565499/filing-history?category=accounts" target="_blank" rel="noopener">English Sangha Trust</a> (charity 231310), <a href="https://find-and-update.company-information.service.gov.uk/company/06688355/filing-history?category=accounts" target="_blank" rel="noopener">Harnham Buddhist Monastery Trust</a> (charity 1126476), <a href="https://find-and-update.company-information.service.gov.uk/company/07387479/filing-history?category=accounts" target="_blank" rel="noopener">Hartridge Buddhist Monastery Trust</a> (charity 1142439). <span class="tag">Updated {datetime.datetime.now(datetime.timezone.utc).strftime("%-d %B %Y, %H:%M GMT")}</span></p>
</section>
</main>
'''
full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + (here / 'head.tmp').read_text().replace('</style>', '</style>\n</head>\n<body>', 1) + body + '\n</body>\n</html>\n')
(here / 'index.html').write_text(full, encoding='utf-8')
back = '<p class="back"><a href="../index.html">← All three trusts</a></p>'
for k, f in FILES.items():
    h = (A[k] / f).read_text(encoding='utf-8')
    assert '<main id="top">' in h, k
    (here / 'pages' / f'{k}.html').write_text(h.replace('<main id="top">', '<main id="top">\n' + back, 1), encoding='utf-8')
for k in fig:
    print(k, fig[k]['years'], r1000(fig[k]['year']), r5(fig[k]['day']), round(fig[k]['people']))
print('wrote index.html and pages/')
