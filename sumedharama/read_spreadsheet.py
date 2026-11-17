# Reads the community's accounts spreadsheet (2012-2024) and writes spreadsheet.json: every expense line per year,
# paired with the matching line of the two-page report (report row numbers as in make_data.py).
# Needs xlrd (pip install xlrd). The spreadsheet itself is not kept in this repo; only these figures.
import json, sys, xlrd
src = sys.argv[1]
b = xlrd.open_workbook(src)
e = b.sheet_by_name('EXPENSES HOUSE')
hdr = {int(c.value): i for i, c in enumerate(e.row(2)) if isinstance(c.value, float)}
# spreadsheet row (0-based) -> report row (index in make_data.rows)
PAIR = {5: 1, 6: 2, 7: 3, 8: 4, 9: 5, 10: 6, 11: 7, 12: 8, 13: 9, 14: 10, 15: 11, 16: 12, 17: 14, 19: 15, 20: 16, 22: 17, 23: 18,
        24: 19, 25: 20, 26: 21, 28: 22, 29: 23, 30: 24, 31: 25, 32: 26, 33: 27, 34: 28, 36: 29, 37: 30, 38: 31, 39: 32, 42: 33,
        43: 34, 44: 35, 45: 36, 47: 37, 48: 38, 49: 39, 50: 40, 51: 41, 52: 42, 53: 43, 54: 44, 56: 45, 57: 46, 58: 47, 59: 48, 61: 49}
out = {'rows': {}}
for sr, rr in PAIR.items():
    d = {str(y): round(e.cell_value(sr, i), 2) for y, i in hdr.items() if isinstance(e.cell_value(sr, i), float)}
    out['rows'][str(rr)] = [e.cell_value(sr, 1), d]
# the separate 2015 sheet has "Clearing land" 6,360.00, which the main sheet leaves out
s15 = b.sheet_by_name('2015 expenses')
cl = [s15.cell_value(r, 2) for r in range(s15.nrows) if 'Clearing land' in str(s15.cell_value(r, 1))]
out['clearing_land_2015'] = cl[0] if cl else None
json.dump(out, open('spreadsheet.json', 'w'), indent=1, ensure_ascii=False)
print('wrote spreadsheet.json', len(out['rows']), 'lines; 2015 clearing land', out['clearing_land_2015'])
