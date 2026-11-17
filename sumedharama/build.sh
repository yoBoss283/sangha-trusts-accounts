#!/bin/sh
# Rebuild from report.pdf. Stops if the report's own totals stop matching the data.
set -e
cd "$(dirname "$0")"
python3 extract_report.py        # needs pypdf (venv/bin/python if you have the venv)
python3 make_data.py
python3 cpi.py
[ -f '../Sangha statistics/entries_fixed.json' ] && python3 people.py > /dev/null   # else keep the saved people.json
python3 build.py
