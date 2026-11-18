#!/usr/bin/env python3
"""Yearly resident counts for the lighter pages (abhayagiri, tisarana, bodhinyanarama).  Usage:
  python3 simple_people.py <folder> <section in the community lists> <dec|mar> [path to entries_fixed.json]
Source: entries_fixed.json of the owner's private Sangha statistics project (default ../Sangha statistics/ or
~/Documents/Sangha statistics/). Counted: monks, novices, nuns, anagarikas in that section (not lay residents or guests).
Year ends 31 December: the year's lists are the Winter list of January (W<year-1>) and the Vassa list of July (V<year>).
Year ends 31 March: the Vassa list of July (V<year-1>) and the Winter list of the next January (W<year-1>).
With both the year gets their average, with one that one, with none no figure. Only these yearly totals are kept, never names.
Writes <folder>/people.json {year: {"people": average, "lists": [codes], "seniors": monks and nuns with 20+ vassa}}."""
import json, pathlib, sys, collections
here = pathlib.Path(__file__).parent
folder, PLACE, ye = sys.argv[1:4]
cands = [pathlib.Path(sys.argv[4])] if len(sys.argv) > 4 else [here.parent / 'Sangha statistics' / 'entries_fixed.json', pathlib.Path.home() / 'Documents' / 'Sangha statistics' / 'entries_fixed.json']
src = next(c for c in cands if c.exists())
E_ = json.load(open(src, encoding='utf-8'))['entries']
KINDS = {'bhikkhu', 'samanera', 'anagarika', 'nun', 'nun_novice'}
per_list, seniors = collections.Counter(), collections.Counter()
for e in E_:
    if e['section'] == PLACE and e['status'] in KINDS:
        per_list[e['season']] += 1
        if e['status'] in ('bhikkhu', 'nun') and (e.get('vassa') or 0) >= 20:
            seniors[e['season']] += 1
out = {}
for y in range(1990, 2100):
    want = (f'W{y - 1}', f'V{y}') if ye == 'dec' else (f'V{y - 1}', f'W{y - 1}')
    codes = [c for c in want if c in per_list]
    if codes:
        out[y] = {'people': round(sum(per_list[c] for c in codes) / len(codes), 1), 'lists': codes,
                  'seniors': round(sum(seniors[c] for c in codes) / len(codes), 1)}
json.dump(out, open(here / folder / 'people.json', 'w', encoding='utf-8'), indent=1)
print(f'{folder}/people.json: {min(out)}-{max(out)}', {y: r['people'] for y, r in out.items() if y >= 2010})
