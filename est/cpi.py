# Prices index for "in today's money": the ONS consumer prices index (CPI, series D7BT, 2015 = 100), saved as
# ons_cpi_d7bt.csv from https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23
# The Trust's year runs April to March, so each year's index is the average of its twelve months.
# Writes cpi.json {year: index}. To update, download the CSV again from that page and rerun.
# Also energy.json: the same for household energy prices, CPI 04.5 "electricity, gas and other fuels" (series D7CH,
# ons_energy_d7ch.csv from https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7ch/mm23), to check the
# heating bill against energy prices. ons_electricity_d7dt.csv (CPI 04.5.1, electricity alone) is kept for reference.
import csv, json, pathlib
here = pathlib.Path(__file__).parent
M = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
def yearly(csvname):
    month = {}
    for row in csv.reader(open(here / csvname, encoding='utf-8')):
        parts = row[0].split() if row else []
        if len(parts) == 2 and parts[0].isdigit() and parts[1] in M:
            month[(int(parts[0]), M.index(parts[1]) + 1)] = float(row[1])
    out = {}
    for y in range(1980, 2100):
        ms = [(y - 1, m) for m in range(4, 13)] + [(y, m) for m in range(1, 4)]
        if all(k in month for k in ms):
            out[y] = round(sum(month[k] for k in ms) / 12, 2)
    return out
for csvname, name in [('ons_cpi_d7bt.csv', 'cpi.json'), ('ons_energy_d7ch.csv', 'energy.json')]:
    out = yearly(csvname)
    json.dump(out, open(here / name, 'w'), indent=0)
    print(f'{name}: years to March {min(out)}–{max(out)}')
