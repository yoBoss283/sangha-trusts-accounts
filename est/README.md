# English Sangha Trust accounts: statistics page

A one-page report of the Trust's money from its published annual accounts (Report of the Trustees and financial
statements), in the same style as the Sangha community list statistics.

## Pipeline

1. `accounts/` holds the annual report PDFs, one per year, with the year in the file name: the Trust's own copies
   (2021–2025, from the Charity Commission) and the scans filed at Companies House (company 00565499, 1995–2026).
2. `extract.py` turns each PDF into text: `txt/<year>.txt`. Scans (no text in the PDF) are read with `ocr.swift`, the
   Mac's own text recognition, and laid out again in columns. When two copies cover a year, the Trust's own is used.
3. `figures.py` reads the figures (group figures only) and writes `data.json`. Each report gives its own year and the
   year before, so most years are read twice; the two readings are compared and every total is checked to add up.
   A year's figures come from its own report, unless that report is a scan (`SCANNED` in `figures.py`).
   `corrections.txt` sets single figures by hand where only a poor scan exists, each with its reason.
   Years before 2020 come only from `read_by_hand.txt`: the core figures read by eye from the scans (the old layouts and
   the auditor's tick marks over digits defeat the automatic reader). The same checks run on them.
   `cpi.py` turns the ONS consumer prices index (`ons_cpi_d7bt.csv`) into April–March averages for "in today's money".
4. `build.py` fills `template.html` and writes `est-accounts.html` (works on its own, offline) and
   `est-accounts-page.html` (the same for publishing as a Claude artifact).

`sh build.sh` runs all three steps and stops if a total does not add up.

Setup: `python3 -m venv venv && venv/bin/pip install -r requirements.txt` (the PDFs are encrypted for printing only;
`cryptography` lets pypdf read them).

## Adding a new year's accounts

1. Put the new PDF in `accounts/` (keep the year in the name, e.g. `English_Sangha_Trust_Accounts_and_TAR_2026.pdf`).
2. `sh build.sh`. Read the "two copies differ" list and fix anything in "Checks".
3. Open `est-accounts.html` and read the new numbers against the report.
4. Hand-written sentences that may need a fresh look: the lede of "3. Money in and money out" (the big gift years),
   and the split of the year's wear on buildings under "How the accounts work it out" (from note 11, charge for the year).
5. Residents: `people.py` reads the Sangha statistics repo (`../Sangha statistics/entries_fixed.json`); run that repo's
   update first if a new community list came in. Without it, the saved `people.json` is used.
