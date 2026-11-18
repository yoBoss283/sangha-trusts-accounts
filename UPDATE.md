# Updating the reports when new accounts come out

Written for the next person or AI that has to do this. The owner only needs to say:
**"Check the repo and update it with any new annual reports, follow UPDATE.md."**

Read `README.md` first (what is here and the rules every page follows), then follow the steps below.
Never skip step 0: it tells you what is already done, so you do not redo or break anything.

## 0. See what is already there

```sh
git pull --rebase            # in the Terminal panel: others may have pushed (the GitHub login is in the keychain)
python3 status.py            # read-only: latest year saved for each place, and what is missing
```

`status.py` prints, for each place, the latest year in the saved figures, the latest accounts PDF in `accounts/`, the
latest year of the price index and of the resident counts, and any `TO DO` line. When every place says "ok", nothing saved
is missing. It **cannot** see whether a newer report has been published; that is step 1.

## 0b. Keep a copy of the current site first (before changing anything)

```sh
python3 archive.py            # saves the site as it is now into archive/<this year-month>/, e.g. archive/2026-11/
```

This copies `index.html` and `pages/*.html` as they are published now, adds an "Archived copy: the site as published in
<month year>. See the latest version" line at the top of each, and does not touch the live pages. After the update,
`sh build_all.sh` adds a line "Earlier versions: <month year>, …" to the small print of the landing page, so readers can look
back at what was said before the newest reports came out. Do this **once per update, before** adding new reports; it refuses
to overwrite an existing copy. Commit the new `archive/` folder together with the update. Never edit or delete old copies.

## 1. Look for new reports

The next report to look for is the year after the latest one `status.py` shows.

| Place | Year ends | Where the report is | Usually filed |
|---|---|---|---|
| English Sangha Trust (`est/`) | 31 March (named by the year it ends in: "2027" = April 2026 to March 2027) | [Companies House 00565499](https://find-and-update.company-information.service.gov.uk/company/00565499/filing-history?category=accounts), [Charity Commission 231310](https://register-of-charities.charitycommission.gov.uk/en/charity-search/-/charity-details/231310/accounts-and-annual-returns) | within about 9–10 months of the year end, so around the end of the calendar year |
| Aruna Ratanagiri (`aruna-ratanagiri/`) | 31 December | [Companies House 06688355](https://find-and-update.company-information.service.gov.uk/company/06688355/filing-history?category=accounts), [Charity Commission 1126476](https://register-of-charities.charitycommission.gov.uk/en/charity-search/-/charity-details/4041769/accounts-and-annual-returns) | within about 9–10 months, so by autumn of the next year |
| Hartridge (`hartridge/`) | 31 December | [Companies House 07387479](https://find-and-update.company-information.service.gov.uk/company/07387479/filing-history?category=accounts), [Charity Commission 1142439](https://register-of-charities.charitycommission.gov.uk/en/charity-search/-/charity-details/5015597/accounts-and-annual-returns) | as above |
| Sumedharama (`sumedharama/`) | 31 December, **euros** | not published: the community's own accounts spreadsheet / "Report to Abbots", shared by Ajahn Vajiro | ask the owner to ask the community |

If the next year's report is not there yet, say so and stop for that place. Do not estimate a year.

**Downloading.** Companies House and the Charity Commission are public, but ask the owner before downloading any file
(say the file name, source and size), unless they have said yes in advance. Never download from anywhere else.

## 2. Add a year to the three UK trusts

1. Put the PDF in that folder's `accounts/`, with the year in the file name, like the others
   (`Companies_House_accounts_2026.pdf`; for the English Sangha Trust, `English_Sangha_Trust_Accounts_and_TAR_2027.pdf`).
2. Set up Python once if the folder has no `venv` (it is not kept in the repo):
   `cd <folder> && python3 -m venv venv && venv/bin/pip install -r requirements.txt`. Needs Python 3.12 or newer and a Mac
   (scans are read with the Mac's own text recognition, `ocr.swift`).
3. Rebuild from the documents: `cd <folder> && sh build.sh`. It reads the PDF, works out the figures, **stops if a total
   does not add up**, and writes the page. Read the "two copies differ" list and the "Checks" it prints.
4. **Scans that cannot be read for sure** (most pre-2020 pages) are never guessed. List each doubtful figure with the PDF
   page and the scan line, ask the owner, and only then enter it in `read_by_hand.txt` or `corrections.txt` with the
   reason. Mark confirmed ones "checked". The owner confirms; you do not.
5. Compare the new year with the report itself: open the built page and read the new numbers against the PDF.

Each folder's own `README.md` describes its scripts. The English Sangha Trust one (`est/README.md`) also names the few
hand-written sentences that may need a fresh look after a new year (the lede of "Money in and money out" and the split of
the year's wear on buildings).

## 3. Add a year to Sumedharama

The community sends a newer accounts spreadsheet or report. Put it in `sumedharama/` (the report as `report.pdf`, the
spreadsheet read by `read_spreadsheet.py`), run `extract_report.py` / `read_spreadsheet.py`, then `make_data.py`. It
lists any year where the report's own lines do not match its totals (`CHECK_THESE_YEARS.md`) and writes the lettered
footnotes. Send the owner the list of differences to check with the community. See `sumedharama/README.md`.

## 3b. The lighter pages (Abhayagiri, Tisarana, Bodhinyanarama)

These three come from totals only and are built by `simple_build.py` from `simple/template.html`. Each folder has `place.json`
(names, currency, notes, sources: edit the notes when something changes), `data.json` (one entry per year: `income`, `spending`,
and where the source gives them `depr`, `cash`, `restricted`, `net_assets`, `gifts`), `people.json` and `cpi_worldbank.json`.

- **Abhayagiri** (`abhayagiri/`, Sanghapala Foundation, US tax number 94-3212705): the yearly totals come from the ProPublica
  Nonprofit Explorer API, `https://projects.propublica.org/nonprofits/api/v2/organizations/943212705.json`; save it as
  `propublica_943212705.json` and rebuild `data.json` from `filings_with_data` (`totrevenue` = income, `totfuncexpns` = spending,
  `totcntrbgfts` = gifts, `totnetassetend` = net assets). The summary data run about a year behind: a newer return may be listed
  only as a PDF (`filings_without_data`). **The PDF download pages are behind a bot check, so do not try to get around it:** ask
  the owner to download the PDF in a browser and put it in `abhayagiri/accounts/`, then read the figures from its first page
  (total revenue line 12, total expenses line 18, net assets line 22) and tell the owner which figures you read. The 2024 return
  and the 2001–2010 returns still need this.
- **Tisarana** (`tisarana/`): the monastery publishes its statements as PDFs on tisarana.ca (find them with
  `https://tisarana.ca/wp-json/wp/v2/media?search=financ&per_page=50`). Put the new year in `accounts/`, read total income,
  total expenses, amortization, cash (chequing + savings), restricted (deferred) money and net assets into `data.json`, and
  cross-check against the "last year" column of the next report. Scanned years are read from the next year's report.
- **Bodhinyanarama** (`bodhinyanarama/`): total income and total expenditure per year from
  `https://register.charities.govt.nz/Charity/CC29078` (annual return table; copy just the table into
  `register_returns.txt`: the whole page names the officers). The year ends 31 March; the return is due by 30 September.
- Residents for all three: `python3 simple_people.py <folder> <Section name in the lists> <dec|mar>` (Abhayagiri / Tisarana
  dec; Bodhinyanarama mar).
- Prices: `cpi_worldbank.json` is the World Bank's yearly consumer price index (`https://api.worldbank.org/v2/country/USA/indicator/FP.CPI.TOTL?format=json&per_page=100`; `CAN`, `NZL` for the others). It runs about a year behind (United States to 2024, the others to 2025).
- Then `python3 simple_build.py` and `sh build_all.sh`.

- **The four Australian monasteries** (`wat-buddha-dhamma/`, `vimokkharam/`, `bodhipala/`, `dhammagiri/`): the figures are the ACNC's
  published Annual Information Statement (AIS) data, one file for each year on data.gov.au (find the datasets with
  `https://data.gov.au/data/api/3/action/package_search?q=acnc+annual+information+statement`; since 2019 there is a CSV for each
  year, `datadotgov_ais<yy>.csv`). Pick the rows of the four ABNs (Wat Buddha Dhamma Foundation Limited 41081615992, Vimokkharam
  Forest Hermitage Inc 73051793658, Bodhipala Monastery Ltd 76627533475, Brisbane Buddhist Vihara (Temple) Inc. 84358631510,
  which runs Dhammagiri) and copy `total gross income`, `total expenses`, `total assets`, `total liabilities` and
  `net assets/liabilities` into `data.json` and `acnc_ais.csv` (the AIS file is large, 30–40 MB: do not keep it in the repo). The
  statements for a year ending 30 June come out about a year later (the 2025 files are due around the end of 2026).
  Years before 2017 have different column names and were not read. The ACNC's data for **Vimokkharam 2021** gives total assets of
  $74 million, a data-entry error that is left out; check any figure that jumps. Dhammagiri's charity is a "basic religious
  charity" from 2024. Price index: `cpi_worldbank.json` with `AUS`. Residents: `simple_people.py` with `dec` (Dhammagiri) or `jun`.

Looked at and not possible (17 Nov 2026): **Temple Forest** (Jetavana Monastic Community, New Hampshire) files no tax returns
publicly; **Santacittarama** (Italy) and **Dhammapala** (Switzerland) have no public accounts that could be found. **Bodhivana** (Victoria, 13 residents) could not be matched to a charity on the ACNC register (no entry with that name), so it is not
included; if its legal name is found, add it like the other Australian pages.

## 4. Refresh the prices (every update)

"In today's money" needs the price index to reach the new year, or the figures cannot be compared.

- **UK pages:** download the ONS series again (CPI, `D7BT`; energy `D7CH`) from the links at the top of each folder's
  `cpi.py`, save over `ons_cpi_d7bt.csv` / `ons_energy_d7ch.csv`, and run `venv/bin/python cpi.py`. The English Sangha
  Trust averages April–March; the other two use calendar years.
- **Sumedharama:** `python3 cpi.py` downloads Portugal's HICP from Eurostat (needs the internet).

## 5. Refresh the number of residents

`people.py` reads the corrected list entries in the owner's separate private project `~/Documents/Sangha statistics`
(`entries_fixed.json`). Only the yearly totals go into the repo (`people.json`); never copy names or lists here.

1. In `~/Documents/Sangha statistics`, follow its own `UPDATE.md` if a new community list has come in.
2. Then, in each folder: `venv/bin/python people.py "$HOME/Documents/Sangha statistics/entries_fixed.json"`.
3. If that project is not available, keep the saved `people.json` and say the residents for the new year are missing.

## 6. Rebuild the landing page and check

```sh
sh build_all.sh              # rebuilds each page from its saved data, then index.html and pages/
python3 status.py            # every place should say ok
```

Then **read the result**: open `index.html` and each changed page, read the changed numbers and check that they make
sense against the reports. The cards, headline figures and "latest year" sentences follow the data. The hand-written
sentences that can go out of date: anything naming a year or an amount in `template.html` that is not computed. Search
the templates for the previous year and for "£" or "€" in plain text, and for each decide whether it still holds.
Keep the wording the owner agreed: plain language, each trust's own cost-line names, and no conclusions stated outright.

## 7. Publish

The site is GitHub Pages from `main`: https://yoboss283.github.io/sangha-trusts-accounts/ .

```sh
git add -A
git -c user.name=yoBoss283 -c user.email=yoBoss283@users.noreply.github.com commit -m "Add <place> <year>"
git pull --rebase && git push          # in the Terminal panel
```

- Commit only with the GitHub no-reply identity above. Never the owner's real name or e-mail anywhere in the repo.
- Rebuild (`sh build_all.sh`) right before committing, because the "Updated" stamp is written at build time.
- Ask the owner before pushing, unless they have said to go ahead.
- If a push is refused because someone else pushed first: pull, rebuild, push again. For conflicts in built files
  (`*.json`, `*.html`), do not merge by hand: settle the source files (`*.py`, `template.html`, docs), then rebuild.

## 8. Tell the owner

Say which places were updated (and to which year), which were not yet available, which figures were read by eye and need
their check, what changed in the headline numbers, and what you could not verify.
