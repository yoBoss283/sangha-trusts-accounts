# Aruna Ratanagiri (Harnham Buddhist Monastery Trust, charity 1126476, company 06688355): accounts statistics

A one-page, plain-language report of what it costs to run the monastery, from the trust's published annual accounts
(2009–2025, all scans at Companies House, years January to December). Part of https://yoboss283.github.io/sangha-trusts-accounts/ .

- `ratanagiri-accounts.html`: the finished page (works on its own, offline). `ratanagiri-accounts-page.html` is the same without the outer html skeleton.
- `accounts/`: the annual report PDFs, year in the file name. `txt/`: their text, made by `extract.py` (scans are read with the
  Mac's text recognition, `ocr.swift`).
- `read_by_hand.txt`, `corrections.txt`: the figures read by eye from the page images (`page.swift` saves a page as a picture),
  each with its source and reason. `figures.py` reads them into `data.json` and stops if a total doesn't add up.
- `cpi.py`: ONS consumer prices (`ons_cpi_d7bt.csv`, energy `ons_energy_d7ch.csv`) averaged over each calendar year.
- `people.py`: yearly resident counts from the Sangha community lists (only the yearly totals are kept, in `people.json`).
- `build.py`: fills `template.html` with the data.

Setup: `python3 -m venv venv && venv/bin/pip install -r requirements.txt`, then `sh build.sh`.
Figures are as paid at the time; "in today's money" uses the price index. No figures per person.
