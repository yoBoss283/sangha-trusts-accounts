# Fill template.html with data.json and write the report in two forms:
#   sumedharama-accounts.html       the full page, works on its own (open it in any browser, also offline)
#   sumedharama-accounts-page.html  the same without the outer <html> skeleton
import json, pathlib, datetime
here = pathlib.Path(__file__).parent
raw = json.load(open(here / 'data.json', encoding='utf-8'))
ppl = json.load(open(here / 'people.json'))
years = sorted(map(int, raw))
data = {}
for y in years:
    r = dict(raw[str(y)])
    r['people'] = ppl[str(y)]['people']
    data[str(y)] = r
d = {'years': years, 'notes': json.load(open(here / 'footnotes.json')), 'data': data, 'cpi': json.load(open(here / 'cpi.json')), 'energy': json.load(open(here / 'energy.json'))}
t = (here / 'template.html').read_text(encoding='utf-8')
for k, v in {'__FIRSTY__': str(years[0]), '__LASTY__': str(years[-1]),
             '__UPDATED__': datetime.datetime.now(datetime.timezone.utc).strftime('%-d %B %Y, %H:%M GMT')}.items():
    t = t.replace(k, v)
t = t.replace('__DATA__', json.dumps(d, ensure_ascii=False).replace('</', '<\\/'))
(here / 'sumedharama-accounts-page.html').write_text(t, encoding='utf-8')
full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + t.replace('</style>', '</style>\n</head>\n<body>', 1) + '\n</body>\n</html>\n')
(here / 'sumedharama-accounts.html').write_text(full, encoding='utf-8')
print('wrote sumedharama-accounts.html and sumedharama-accounts-page.html')
