#!/bin/sh
# Rebuild everything from the PDFs in accounts/. Stops if a total doesn't add up.
set -e
cd "$(dirname "$0")"
venv/bin/python extract.py
venv/bin/python figures.py
venv/bin/python cpi.py
[ -f '../Sangha statistics/entries_fixed.json' ] && venv/bin/python people.py > /dev/null   # else keep the saved people.json
venv/bin/python build.py
