# Fill template.html with data.json and write the report in two forms:
#   ratanagiri-accounts.html       the full page, works on its own (open it in any browser, also offline)
#   ratanagiri-accounts-page.html  the same without the outer <html> skeleton, for publishing as a Claude artifact
# Words like __LASTY__ in the template follow the data, so a new year's accounts need no hand edits of years.
import json, pathlib, datetime, sys
here = pathlib.Path(__file__).parent
START = 2011              # 2010 was the year the trust took over from the Magga Bhavaka Trust (a setup year)
raw = json.load(open(here / 'data.json', encoding='utf-8'))
ppl = json.load(open(here / 'people.json'))
years = [y for y in sorted(map(int, raw)) if y >= START]
data = {}
for y in years:
    r = dict(raw[str(y)])
    if str(y) in ppl:
        r['people'] = ppl[str(y)]['people']
        r['seniors'] = ppl[str(y)]['seniors']
    data[str(y)] = r

# every cost line must belong to exactly one kind on the page (template.html, KINDS), and the kinds plus depreciation
# and the loss on disposals must make up total spending
KINDS = {'heat': 'heat', 'repairs': 'repairs', 'rent': 'rri', 'ins': 'rri',
         'welfare': 'whf', 'household': 'whf', 'breakfast': 'whf', 'kitchen': 'whf', 'motor': 'car', 'travel': 'car',
         'events': 'teach', 'pubs': 'teach', 'dana': 'teach', 'religious': 'teach',
         'staff': 'office', 'office': 'office', 'phone': 'office', 'legal': 'office', 'bank': 'office', 'gov': 'office',
         'sundry': 'office', 'misc': 'office', 'mbt': 'office'}
NOT_RUNNING = {'depr', 'disposal'}
OTHER_KEYS = {'income', 'spending', 'gov_sofa', 'capex', 'people', 'seniors'}
bad = []
for y, r in data.items():
    bad += [f'{y}: {k} is in no kind' for k in r if k not in KINDS and k not in NOT_RUNNING and k not in OTHER_KEYS]
    total = sum(v for k, v in r.items() if k in KINDS or k in NOT_RUNNING)
    if abs(total - r['spending']) > 2:
        bad.append(f'{y}: cost lines {total:,} against total spending {r["spending"]:,}')
if bad:
    sys.exit('build.py: ' + '; '.join(map(str, bad)))

d = {'years': years, 'data': data, 'cpi': json.load(open(here / 'cpi.json')), 'energy': json.load(open(here / 'energy.json'))}
tokens = {
    '__FIRSTY__': str(years[0]),
    '__LASTY__': str(years[-1]),
    '__UPDATED__': datetime.datetime.now(datetime.timezone.utc).strftime('%-d %B %Y, %H:%M GMT'),
}
t = (here / 'template.html').read_text(encoding='utf-8')
for k, v in tokens.items():
    t = t.replace(k, v)
t = t.replace('__DATA__', json.dumps(d, ensure_ascii=False).replace('</', '<\\/'))   # the data last, so nothing in it is touched
(here / 'ratanagiri-accounts-page.html').write_text(t, encoding='utf-8')
full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + t.replace('</style>', '</style>\n</head>\n<body>', 1) + '\n</body>\n</html>\n')
(here / 'ratanagiri-accounts.html').write_text(full, encoding='utf-8')
print('wrote ratanagiri-accounts.html and ratanagiri-accounts-page.html')
