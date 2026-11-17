# Fill template.html with data.json and write the report in two forms:
#   est-accounts.html       the full page, works on its own (open it in any browser, also offline)
#   est-accounts-page.html  the same without the outer <html> skeleton
# Words like __LASTY__ in the template follow the data, so a new year's accounts need no hand edits of years.
import json, pathlib, datetime
here = pathlib.Path(__file__).parent
d = json.load(open(here / 'data.json', encoding='utf-8'))
START = 2002                                                   # the page shows the years to March 2002 on: the first year with
d['years'] = [y for y in d['years'] if y >= START]               # resident counts for every list. data.json keeps all years.
d['data'] = {y: r for y, r in d['data'].items() if int(y) >= START}
d['cpi'] = json.load(open(here / 'cpi.json'))
d['energy'] = json.load(open(here / 'energy.json'))          # energy prices index (cpi.py), for the heating bill
ppl = json.load(open(here / 'people.json'))                    # residents per Trust year (people.py, from the community lists)
for y, r in ppl.items():
    if y in d['data']:
        d['data'][y]['people'] = r['people']
        d['data'][y]['seniors'] = r.get('seniors')                 # prices index, for "in today's money" (cpi.py)
reports = sorted(int(p.stem) for p in (here / 'txt').glob('*.txt'))
from figures import SCANNED
tokens = {
    '__FIRSTY__': str(d['years'][0]),
    '__LASTY__': str(d['years'][-1]),
    '__FIRSTREPORT__': str(reports[0]),
    '__SCANNED__': ' and '.join(str(y) for y in sorted(SCANNED)),
    '__UPDATED__': datetime.datetime.now(datetime.timezone.utc).strftime('%-d %B %Y, %H:%M GMT'),
}
t = (here / 'template.html').read_text(encoding='utf-8')
for k, v in tokens.items():
    t = t.replace(k, v)
t = t.replace('__DATA__', json.dumps(d, ensure_ascii=False).replace('</', '<\\/'))   # the data last, so nothing in it is touched
(here / 'est-accounts-page.html').write_text(t, encoding='utf-8')
full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + t.replace('</style>', '</style>\n</head>\n<body>', 1) + '\n</body>\n</html>\n')
(here / 'est-accounts.html').write_text(full, encoding='utf-8')
print('wrote est-accounts.html and est-accounts-page.html')
