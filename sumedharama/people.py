# How many people live at Sumedharama, per calendar year, from the Sangha community lists.
# Source: entries_fixed.json in the Sangha statistics repo (~/Documents/Sangha statistics), the corrected list entries.
# Counted: everyone in the "Sumedharama" section who is a bhikkhu, nun, sāmaṇera, anagārika/anagārikā or novice.
# Not counted: lay residents and guests (Kusala House), visitors.
# The Trust's year runs January to December and holds one Winter list (January: code W<year-1>, the list that follows
# the Vassa list of the year before) and one Vassa list (July: code V<year>). With both the year gets their average;
# with one, that one; with none, no figure. Only these yearly totals leave the Sangha repo, never names or entries.
# Writes people.json {year: {"people": average, "lists": [codes], "seniors": monks with 20+ vassa, average}}.
import json, pathlib, sys, collections
here = pathlib.Path(__file__).parent
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else here.parent / 'Sangha statistics' / 'entries_fixed.json')
E = json.load(open(src, encoding='utf-8'))['entries']
PLACE = 'Sumedharama'
KINDS = {'bhikkhu', 'samanera', 'anagarika', 'nun', 'nun_novice'}
per_list, seniors = collections.Counter(), collections.Counter()
for e in E:
    if e['section'] == PLACE and e['status'] in KINDS:
        per_list[e['season']] += 1
        if e['status'] in ('bhikkhu', 'nun') and (e.get('vassa') or 0) >= 20:
            seniors[e['season']] += 1
out = {}
for y in range(1990, 2100):
    codes = [c for c in (f'W{y - 1}', f'V{y}') if c in per_list]
    if codes:
        out[y] = {'people': round(sum(per_list[c] for c in codes) / len(codes), 1), 'lists': codes,
                  'seniors': round(sum(seniors[c] for c in codes) / len(codes), 1)}
json.dump(out, open(here / 'people.json', 'w', encoding='utf-8'), indent=1)
print(f'people.json: {min(out)}–{max(out)} from {src}')
for y, r in out.items():
    if y >= 2009:
        print(y, r['people'], r['lists'], r['seniors'])
