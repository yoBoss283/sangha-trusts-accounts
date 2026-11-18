#!/usr/bin/env python3
"""Where is each report? Read-only: changes nothing. Run:  python3 status.py

For each monastery it prints the latest year in the saved figures (data.json), the latest accounts PDF in accounts/,
the latest year of the price index and of the resident counts, and says what is missing. Then it checks that the
built pages are newer than the data. Add a year following UPDATE.md; run this again afterwards: every line should say ok.
"""
import json, re, pathlib, datetime
here = pathlib.Path(__file__).parent

def years(obj):
    if isinstance(obj, dict) and 'data' in obj and isinstance(obj['data'], dict): obj = obj['data']
    return sorted(int(k) for k in obj if re.fullmatch(r'\d{4}', str(k))) if isinstance(obj, dict) else []

PLACES = {  # folder: (name, year ends, built page, where the new report comes from)
    'est': ('English Sangha Trust (Amaravati, Chithurst)', '31 March', 'est-accounts.html', 'Companies House 00565499 / Charity Commission 231310'),
    'aruna-ratanagiri': ('Aruna Ratanagiri (Harnham)', '31 December', 'ratanagiri-accounts.html', 'Companies House 06688355 / Charity Commission 1126476'),
    'hartridge': ('Hartridge', '31 December', 'hartridge-accounts.html', 'Companies House 07387479 / Charity Commission 1142439'),
    'abhayagiri': ('Abhayagiri (California, US dollars)', '31 December', 'abhayagiri-accounts.html', 'ProPublica Nonprofit Explorer, Sanghapala Foundation 94-3212705 (the summary data run about a year behind: later returns are PDFs)'),
    'tisarana': ('Tisarana (Ontario, Canadian dollars)', '31 December', 'tisarana-accounts.html', 'the financial statements on tisarana.ca (usually published in spring)'),
    'bodhinyanarama': ('Bodhinyanarama (Wellington, NZ dollars)', '31 March', 'bodhinyanarama-accounts.html', 'NZ Charities Register, CC29078 (annual return, due 30 September)'),
    'wat-buddha-dhamma': ('Wat Buddha Dhamma (NSW, Australian dollars)', '30 June', 'wat-buddha-dhamma-accounts.html', 'the ACNC Annual Information Statement data on data.gov.au (the 2025 statements are published about a year later)'),
    'vimokkharam': ('Vimokkharam (Victoria, Australian dollars)', '30 June', 'vimokkharam-accounts.html', 'the ACNC Annual Information Statement data on data.gov.au (the 2025 statements are published about a year later)'),
    'bodhipala': ('Bodhipala (South Australia, Australian dollars)', '30 June', 'bodhipala-accounts.html', 'the ACNC Annual Information Statement data on data.gov.au (the 2025 statements are published about a year later)'),
    'dhammagiri': ('Dhammagiri (Queensland, Australian dollars)', '31 December', 'dhammagiri-accounts.html', 'the ACNC Annual Information Statement data on data.gov.au (the 2025 statements are published about a year later)'),
    'bodhivana': ('Bodhivana (Victoria, Australian dollars)', '30 June', 'bodhivana-accounts.html', 'the ACNC Annual Information Statement data on data.gov.au (ABN 59019586160)'),
    'pacific-hermitage': ('Pacific Hermitage (Washington, US dollars)', '31 December', 'pacific-hermitage-accounts.html', 'ProPublica Nonprofit Explorer, Sanghata Foundation 27-2787286'),
    'milntuim': ('Milntuim (Scotland, pounds)', '31 December', 'milntuim-accounts.html', 'OSCR register SC043482 (accounts filed by 30 September of the next year)'),
    'sumedharama': ('Sumedharama (Portugal, euros)', '31 December', 'sumedharama-accounts.html', 'the community (ask Ajahn Vajiro): updated accounts spreadsheet / report to the abbots'),
}
problems = 0
for d, (name, ye, page, src) in PLACES.items():
    p = here / d
    data = years(json.load(open(p / 'data.json')))
    pdfs = sorted(int(m.group(1)) for f in (p / 'accounts').glob('*.pdf') if (m := re.search(r'(\d{4})', f.name))) if (p / 'accounts').is_dir() else []
    cpi = years(json.load(open(p / ('cpi.json' if (p / 'cpi.json').exists() else 'cpi_worldbank.json')))); ppl = years(json.load(open(p / 'people.json')))
    last = data[-1]
    print(f'\n{name}  (year ends {ye})')
    print(f'  figures: {data[0]}-{last}   price index: to {cpi[-1]}   residents: to {ppl[-1] if ppl else "none"}' + (f'   accounts PDFs: to {pdfs[-1]}' if pdfs else ('   source: saved data, see place.json' if (p / 'place.json').exists() else '   source: report.pdf + spreadsheet.json')))
    notes = []
    if pdfs and pdfs[-1] > last: notes.append(f'a PDF for {pdfs[-1]} is in accounts/ but not in the figures: run the folder\'s build')
    if cpi[-1] < last - (1 if d == 'bodhinyanarama' else 0): notes.append(f'price index stops at {cpi[-1]}: refresh the ONS/Eurostat file (UPDATE.md step 4)')
    if not ppl or ppl[-1] < last: notes.append(f'no resident count for {last}: needs the newest community lists (UPDATE.md step 5)')
    out = p / page
    if out.exists() and (p / 'data.json').stat().st_mtime > out.stat().st_mtime + 1: notes.append('built page is older than data.json: rebuild')
    print('  ' + ('ok: nothing missing in what is saved' if not notes else '\n  '.join('TO DO: ' + n for n in notes)))
    problems += len(notes)
    print(f'  next report to look for: the year after {last} (from {src})')
print('\nAll saved figures, prices and pages are in step.' if not problems else f'\n{problems} thing(s) to do (see TO DO above).')
print('This only checks what is saved here. It cannot see whether a newer report has been published: look at the sources in UPDATE.md.')
