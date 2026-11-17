# Prices for "in today's money": Portugal's harmonised index of consumer prices (HICP), annual averages, from Eurostat
# (dataset prc_hicp_aind, 2015 = 100): all items (CP00) and "electricity, gas and other fuels" (CP045) for the energy check.
# The community's year is the calendar year, so the annual average fits. Writes cpi.json and energy.json {year: index}.
# Run with the internet on to refresh; the downloads are kept in eurostat_hicp_pt.json.
import json, pathlib, urllib.request
here = pathlib.Path(__file__).parent
URL = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_aind?format=JSON&lang=en&geo=PT&unit=INX_A_AVG&coicop={}&sinceTimePeriod=2008'
raw = {}
for code in ('CP00', 'CP045'):
    try:
        raw[code] = json.load(urllib.request.urlopen(URL.format(code), timeout=30))
    except Exception as e:
        raw = json.load(open(here / 'eurostat_hicp_pt.json')); print('offline, using the saved download'); break
else:
    json.dump(raw, open(here / 'eurostat_hicp_pt.json', 'w'))
def yearly(d):
    years = list(d['dimension']['time']['category']['index'])
    return {y: v for y, v in zip(years, [d['value'][str(i)] for i in range(len(years))]) if True}
for code, name in (('CP00', 'cpi.json'), ('CP045', 'energy.json')):
    out = yearly(raw[code]); json.dump(out, open(here / name, 'w'), indent=0)
    print(name, min(out), max(out), out.get('2025'))
