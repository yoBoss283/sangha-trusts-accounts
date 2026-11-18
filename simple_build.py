#!/usr/bin/env python3
"""Build the lighter report pages (abhayagiri, tisarana, bodhinyanarama) from each folder's saved data.
Run:  python3 simple_build.py [folder ...]     (build_all.sh runs it for every folder that has a place.json)
Reads <folder>/place.json (names, currency, notes, sources), data.json (every figure by year), people.json and
cpi_worldbank.json (the price index), fills simple/template.html and writes <folder>/<folder>-accounts.html and -accounts-page.html.
(year ends: dec = calendar year, mar = year to 31 March, jun = year to 30 June)
The pages that come from this template give totals only (money in, spending, what is held): their accounts have no cost-by-cost detail."""
import json, pathlib, sys, datetime
here = pathlib.Path(__file__).parent
FOLDERS = ['abhayagiri', 'tisarana', 'bodhinyanarama', 'wat-buddha-dhamma', 'vimokkharam', 'bodhipala', 'dhammagiri', 'bodhivana', 'pacific-hermitage', 'milntuim', 'temple-forest', 'forest-hermitage', 'lokuttara']

def build(folder):
    p = here / folder
    cfg = json.load(open(p / 'place.json', encoding='utf-8'))
    raw = json.load(open(p / 'data.json', encoding='utf-8'))
    people = json.load(open(p / 'people.json', encoding='utf-8')) if (p / 'people.json').exists() else {}
    wb = json.load(open(p / ('cpi.json' if (p / 'cpi.json').exists() else 'cpi_worldbank.json')))
    years = sorted(int(y) for y in raw)
    cpi, data = {}, {}
    for y in years:
        # price index: the calendar year of the accounts; for a year ending in March, the calendar year in which most of it falls
        ye = cfg.get('yearEnd')
        if ye == 'jun':                              # a year to 30 June: the average of the two calendar years it spans
            cpi[str(y)] = round((wb[str(y - 1)] + wb.get(str(y), wb[str(y - 1)])) / 2, 3)
        else:
            cy = y - 1 if ye == 'mar' else y
            cpi[str(y)] = wb[str(cy)]
        data[str(y)] = dict(raw[str(y)])
        if str(y) in people: data[str(y)]['people'] = people[str(y)]['people']
    D = {k: cfg[k] for k in ['currency', 'currencyName', 'cpiName', 'short', 'runVerb', 'costName', 'costDefShort', 'defs', 'incomeNote', 'meaningNote', 'holdSeries', 'holdSub', 'holdLede', 'holdNote', 'notes', 'sources', 'daysInYear', 'operating'] if k in cfg}
    D.update({'years': years, 'data': data, 'cpi': cpi})
    html = (here / 'simple' / 'template.html').read_text(encoding='utf-8')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%-d %B %Y, %H:%M GMT')
    D['sources'] = D['sources'].replace('__UPDATED__', stamp)
    for k, val in {'__TITLE__': cfg['title'], '__KICKER__': cfg['kicker'], '__SHORT__': cfg['short'], '__FIRSTY__': str(years[0]), '__LASTY__': str(years[-1])}.items():
        html = html.replace(k, val)
    html = html.replace('__DATA__', json.dumps(D, ensure_ascii=False).replace('</', '<\\/'))
    (p / f'{folder}-accounts-page.html').write_text(html, encoding='utf-8')
    full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + html.replace('</style>', '</style>\n</head>\n<body>', 1) + '\n</body>\n</html>\n')
    (p / f'{folder}-accounts.html').write_text(full, encoding='utf-8')
    # the numbers the landing page card shows: the same rules as the page (latest three years; periods of five years back from the latest)
    ys = [str(y) for y in years]
    run = lambda y: data[y]['spending'] - (data[y].get('depr') or 0)
    avg = lambda yy, f: sum(f(y) for y in yy) / len(yy)
    if len(ys) <= 9:
        h = len(ys) // 2; blocks = [ys[:h], ys[h:]]          # a short record: two halves (as in the template)
    else:
        blocks = []; e = len(ys)
        while e > 0:
            blocks.insert(0, ys[max(0, e - 5):e]); e -= 5
        if len(blocks) > 1 and len(blocks[0]) < 3: blocks.pop(0)
    today = lambda y: cpi[ys[-1]] / cpi[y]
    real = lambda b: avg(b, lambda y: run(y) * today(y))
    n3 = ys[-3:]
    lab = lambda b: f'{b[0]}–{b[-1][2:]}'
    facts = {'years': lab(n3), 'year': avg(n3, run), 'income': avg(n3, lambda y: data[y]['income']), 'people': avg(n3, lambda y: data[y].get('people') or 0),
             'pct': round(100 * (real(blocks[-1]) / real(blocks[0]) - 1)), 'from': lab(blocks[0]), 'to': lab(blocks[-1]), 'currency': cfg['currency'], 'operating': cfg.get('operating', True)}
    json.dump(facts, open(p / 'facts.json', 'w'), indent=1)
    print(f'{folder}: {years[0]}-{years[-1]}, {len(html):,} bytes')

for f in (sys.argv[1:] or FOLDERS):
    build(f)
