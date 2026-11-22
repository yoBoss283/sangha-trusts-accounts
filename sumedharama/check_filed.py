#!/usr/bin/env python3
"""Compares data.json with filed_accounts.json (the community's annual accounts, 2014-2024) and prints every difference.
Run: python3 check_filed.py   (after make_data.py). Differences of a euro or two are rounding."""
import json, pathlib
here = pathlib.Path(__file__).parent
d = json.load(open(here / 'data.json')); F = json.load(open(here / 'filed_accounts.json'))['years']
for y, (don, oth, intr, fse, oe, dep, net, ta, eq) in F.items():
    r = d[y]; fin = don + oth + (intr or 0); fsp = fse + oe + dep
    print(y, 'money in', round(r['income'] - fin, 2), '| spending', round(r['spending'] - fsp, 2), '| equity', None if eq is None else round(r['equity'] - eq, 2))
