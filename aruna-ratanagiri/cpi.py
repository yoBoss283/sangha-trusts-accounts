# Prices index for "in today's money": the ONS consumer prices index (CPI, series D7BT, 2015 = 100), saved as
# ons_cpi_d7bt.csv from https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23
# The Trust's year runs January to December, so each year's index is the average of its twelve months.
# Also energy.json: household energy prices, CPI 04.5 (series D7CH, ons_energy_d7ch.csv), to check the heating bill.
# Writes cpi.json and energy.json {year: index}. To update, download the CSVs again and rerun.
import csv, json, pathlib
here = pathlib.Path(__file__).parent
M = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
def yearly(csvname):
    month = {}
    for row in csv.reader(open(here / csvname, encoding='utf-8')):
        parts = row[0].split() if row else []
        if len(parts) == 2 and parts[0].isdigit() and parts[1] in M:
            month[(int(parts[0]), M.index(parts[1]) + 1)] = float(row[1])
    return {y: round(sum(month[(y, m)] for m in range(1, 13)) / 12, 2)
            for y in range(1980, 2100) if all((y, m) in month for m in range(1, 13))}
for csvname, name in [('ons_cpi_d7bt.csv', 'cpi.json'), ('ons_energy_d7ch.csv', 'energy.json')]:
    out = yearly(csvname)
    json.dump(out, open(here / name, 'w'), indent=0)
    print(f'{name}: {min(out)}–{max(out)}')
