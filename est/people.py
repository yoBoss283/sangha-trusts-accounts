# How many people live at the two monasteries the Trust looks after, per Trust year, from the Sangha community lists.
# Source: entries_fixed.json in the Sangha statistics repo (~/Documents/Sangha statistics), the corrected list entries.
# Counted: everyone on the list at Amaravati or Cittaviveka who is a bhikkhu, nun, sāmaṇera, anagārika/anagārikā or
# novice nun. Not counted: lay residents (not every list names them) and visitors.
# A Trust year runs April to March and holds one Vassa list (July) and one Winter list (January):
# the year to March 2026 holds Vassa 2025 (code V2025) and the Winter list of January 2026 (code W2025).
# With both lists the year gets their average; with one, that one; with none, no figure.
# Writes people.json {year: {"people": average, "lists": [codes], "amaravati": avg, "cittaviveka": avg,
# "seniors": monks and nuns with 20+ years in robes (vassa), average}}.
import json, pathlib, sys, collections
here = pathlib.Path(__file__).parent
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else here.parent / 'Sangha statistics' / 'entries_fixed.json')
E = json.load(open(src, encoding='utf-8'))['entries']
PLACES = ('Amaravati', 'Cittaviveka')
KINDS = {'bhikkhu', 'samanera', 'anagarika', 'nun', 'nun_novice'}
per_list = collections.defaultdict(collections.Counter)
seniors = collections.Counter()      # monks and nuns with 20 or more years in robes (vassa), at the two monasteries
for e in E:
    if e['section'] in PLACES and e['status'] in KINDS:
        per_list[e['season']][e['section']] += 1
        if e['status'] in ('bhikkhu', 'nun') and (e.get('vassa') or 0) >= 20:
            seniors[e['season']] += 1
out = {}
for y in range(1990, 2100):
    codes = [c for c in (f'V{y - 1}', f'W{y - 1}') if c in per_list]
    if not codes:
        continue
    avg = lambda f: round(sum(f(per_list[c]) for c in codes) / len(codes), 1)
    out[y] = {'people': avg(lambda n: n['Amaravati'] + n['Cittaviveka']), 'lists': codes,
              'amaravati': avg(lambda n: n['Amaravati']), 'cittaviveka': avg(lambda n: n['Cittaviveka']),
              'seniors': round(sum(seniors[c] for c in codes) / len(codes), 1)}
json.dump(out, open(here / 'people.json', 'w', encoding='utf-8'), indent=1)
print(f'people.json: years to March {min(out)}–{max(out)} from {src}')
for y, r in out.items():
    print(y, r['people'], r['lists'], r['amaravati'], r['cittaviveka'])
