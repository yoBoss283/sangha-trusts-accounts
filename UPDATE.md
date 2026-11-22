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
back at what was said before the newest reports came out. No copy exists yet (the November 2026 version was not final and its copy was removed): the first one is made at the next yearly update. Do this **once per update, before** adding new reports; it refuses
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
footnotes. Send the owner the list of differences to check with the community. See `sumedharama/README.md`. If the community sends annual accounts (balance sheet and profit and loss) for a new year, add its figures to `sumedharama/filed_accounts.json` and run `python3 sumedharama/check_filed.py`: the spreadsheet agreed with the accounts for 2014 to 2024 except 2018, 2020 and 2022.

## 3b. The lighter pages (Abhayagiri, Tisarana, Bodhinyanarama)

These three come from totals only and are built by `simple_build.py` from `simple/template.html`. Each folder has `place.json`
(names, currency, notes, sources: edit the notes when something changes), `data.json` (one entry per year: `income`, `spending`,
and where the source gives them `depr`, `cash`, `restricted`, `net_assets`, `gifts`), `people.json` and `cpi_worldbank.json`.

- **Abhayagiri** (`abhayagiri/`, Sanghapala Foundation, US tax number 94-3212705): 2011 to 2023 come from the ProPublica
  Nonprofit Explorer API, `https://projects.propublica.org/nonprofits/api/v2/organizations/943212705.json`; save it as
  `propublica_943212705.json` (delete the organization's `careofname`, `address` and `zipcode`: they hold a person's name) and rebuild
  `data.json` from `filings_with_data` (`totrevenue` = income, `totfuncexpns` = spending, `totcntrbgfts` = gifts, `totnetassetend` =
  net assets). 2001 to 2010 and 2024 were read by eye from scanned returns (Form 990 line 12 total revenue, 17 or 18 total expenses,
  21 or 22 net assets; OCR with `est/ocr.swift`, `page.swift` to look at a page); check every year against the next return's opening
  net assets. The summary data run about a year behind: a newer return appears first only as a PDF (`filings_without_data`). **The PDF
  download pages are behind a bot check, so do not try to get around it:** ask the owner to download the PDF in a browser into
  `abhayagiri/accounts/` (kept out of git: `abhayagiri/accounts/SOURCES.txt` says why). The 2025 return is the next one. Abhayagiri has a second related charity, the Abhayagiri Monastic Foundation (EIN 72-1537214), named in Schedule R of the 2024 return, that holds fixed assets transferred from the Sanghapala Foundation; ProPublica lists no returns for it.
- **Tisarana** (`tisarana/`): the monastery publishes its statements as PDFs on tisarana.ca (find them with
  `https://tisarana.ca/wp-json/wp/v2/media?search=financ&per_page=50`). Put the new year in `accounts/`, read total income,
  total expenses, amortization, cash (chequing + savings), restricted (deferred) money and net assets into `data.json`, and
  cross-check against the "last year" column of the next report. Scanned years are read from the next year's report.
- **Bodhinyanarama** (`bodhinyanarama/`): total income and total expenditure per year from
  `https://register.charities.govt.nz/Charity/CC29078` (annual return table; copy just the table into
  `register_returns.txt`: the whole page names the officers). The year ends 31 March; the return is due by 30 September.
- **Vimutti** (`vimutti/`, Auckland Theravada Buddhist Association, charity CC20332): same register as Bodhinyanarama (`https://register.charities.govt.nz/Charity/CC20332`; copy just the table into `register_returns.txt`). Year ends 31 July. The register shows $0 or tiny spending for most years before 2023, so the owner chose to show every year from 2012 as filed (zeros included) with a note warning about the low years (21 Nov 2026); 2008 to 2011 are all $0 and not charted. Residents: `simple_people.py vimutti Vimutti dec`. The audited PDFs behind the earlier years were not read (downloads need the owner's OK).
- **Theravada Monastic Trust** (`theravada-monastic-trust/`, charity 1127588; added 21 Nov 2026 at the owner's request): a UK funding trust that passes donations to the monasteries; it runs none and has no residents. Income and expenditure per year from `https://opencharities.uk/ew/1127588.json` (`financial_years`; save it as `opencharities_1127588.json` without email, phone, address). Net assets and the grant lists in the notes come from each year's accounts (`.../ew/1127588/files/<year>-12-31-accounts.md`): update the grants note by hand each year. Its spending is grants paid out, never to be added to the monasteries' costs (the card says so). Uses the UK price index (`cpi.json`).
- **`"operating": false` in `place.json`** marks a place whose accounts give only total expenses, so building work and wear on buildings cannot be
  taken out (everything except Tisarana and Forest Hermitage, which remove depreciation). Its page and landing card then show total
  spending and money in, never a running cost, a cost a day, a cost for each resident or a change after inflation: do not compare
  total spending as if it were operating cost. If a source starts to give depreciation or building work separately, put it in
  `data.json` (`depr`) and drop the flag.
- Residents for all three: `python3 simple_people.py <folder> <Section name in the lists> <dec|mar>` (Abhayagiri / Tisarana
  dec; Bodhinyanarama mar).
- Prices: `cpi_worldbank.json` is the World Bank's yearly consumer price index (`https://api.worldbank.org/v2/country/USA/indicator/FP.CPI.TOTL?format=json&per_page=100`; `CAN`, `NZL` for the others). It runs about a year behind (United States to 2024, the others to 2025).
- Then `python3 simple_build.py` and `sh build_all.sh`.

- **Bodhivana** (`bodhivana/`) is the Victoria Sangha Association Inc. (ABN 59019586160) in the same ACNC data, years 2016 to 2024.
  **Pacific Hermitage** (`pacific-hermitage/`) is the Sanghata Foundation (US tax number 27-2787286): same ProPublica API as
  Abhayagiri (`.../api/v2/organizations/272787286.json`), 2011 to 2023 (do not save the officer or care-of fields of the
  organization record: they hold a person's name). **Milntuim** (`milntuim/`) is Scottish charity SC043482: income and expenditure
  for 2020 to 2025 from `https://opencharities.uk/sc/SC043482.json` (`financial_years`; assets are not in it, the accounts are PDFs
  at the OSCR register); it uses the UK price index (`cpi.json`) and pounds.
- **Lokuttara** (`lokuttara/`) is Stiftelsen Skogskloster, Norway (org. no. 997036034): the figures are open data at
  `https://data.brreg.no/regnskapsregisteret/regnskap/997036034` (saved as `brreg_997036034.json`; one record a year, 2023 onward; `driftsinntekter`,
  `driftskostnad`, `eiendeler`, `egenkapital`). Shown in euros (ECB yearly average rate for each year, in `place.json` under `convert`; add the new year's rate, from `data-api.ecb.europa.eu/service/data/EXR/A.NOK.EUR.SP00.A`), with the kroner in brackets: the one place that is converted, because the owner asked for easy comparison. World Bank price index (`cpi_worldbank.json`), resident counts with
  `simple_people.py lokuttara Lokuttara dec`. Costs probably include depreciation, so it is `operating: false`.
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

- **Temple Forest** (`temple-forest/`) is run through the Jeta Grove Foundation Inc. (US tax number 30-0754003; the monastery's website says
  it handles the monastery's money). Same ProPublica API as Abhayagiri, 2014 to 2020; later returns are only PDFs (ask the owner to download
  them). The Jetavana Monastic Community (83-3987123) is a different body with no returns. **Forest Hermitage** (`forest-hermitage/`) is The Forest
  Hermitage Trust (charity 1173083, company 10368008): its accounts are at Companies House (`.../company/10368008/filing-history?category=accounts`; the
  PDFs are scans, read with `est/ocr.swift`: `swiftc -O est/ocr.swift -o ocr; ./ocr file.pdf`), for the years to March 2019 (comparison column of the 2020 accounts) to 2026;
  the Charity Commission register and `https://opencharities.uk/ew/1173083.json` hold only the last five years and are used to cross-check. The Buddha-Dhamma
  Fellowship (289913) held the monastery's money until April 2019 and is not included (its earlier accounts are not public online). The community lists have no section for it, so
  it has no residents. **Bodhinyanarama** also has treasurer's reports in the AGM minutes on its website (2014 to 2021: net assets, 2014 to 2016
  income); the page is text hidden behind "read more" buttons, so read it in a browser.

Looked at and not possible (17 Nov 2026): **Temple Forest** (Jetavana Monastic Community, New Hampshire) files no tax returns
publicly; **Santacittarama** (Italy) and **Dhammapala** (Switzerland; the body behind it is the "Trägerverein" = Verein Dhammapala, CHE-109.752.928, tax-exempt since 2023; its support page, German and English, gives bank details but no accounts, and the English "Dhammapala Trust" is the same Trägerverein) have no public accounts that could be found. **Santacittarama** (Italy), **Dhammapala** (Switzerland), **Lokuttara** (Norway), **Pannagiri** (Spain) and **Suddhavari** (Brazil): nothing public
found by search (Italian and Swiss associations do not publish accounts the way UK and US charities do). **Three Jewels** is a meditation
hall in Fort Bragg, California that Abhayagiri's monks visit, not a separate monastery with accounts.
Tisarana also publishes an audited statement for 2022 (`https://tisarana.ca/wp-content/uploads/2023/12/2022-Audited-FS-Tisarana-Buddhist-Monastery.pdf`)
that has not been compared with the figures used for 2022 (taken from the 2023 report's last-year column).

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

- **EST "What this means"** has a hand-written phrase that staff cost "has about doubled in the last two years" (2024 £57k → 2025 £106k). Check it against the new year's staff line (`sp_staff`) each update.
- **EST hand-typed staff figures (check every update).** In `est/template.html`:
  - `STAFF_CAP` (in the "next five years" section) holds the staff cost the Trust counted as building work, from note 10 of the accounts: 2024 £50,982, 2025 £50,302, 2026 £22,931. Add the new year, and drop the oldest if the average should stay at three years. The higher estimate and its "Staff:" bullet follow from it. The "£23k–51k a year more is counted as building work" sentences in the staff section and the bridge note are typed too: update their range.
  - The staff section ("Everything else") draws one bar a year for total pay (`salaries` + `nic` + `pension` from the staff note, in the latest year's money) with a dashed line for the staff line (`sp_staff`). The total pay is higher than the staff line because the rest is booked in other cost lines or as building work; the accounts do not show where. The percentage rises ("since 2020") are computed. Do not add total pay on top of the cost lines: that would count some of it twice. If the Trust or its accountants ever give pay by cost line, the chart can be corrected.
  - "What this means" says the staff line "has about doubled in the last two years" (hand-typed) but that total staff pay rose only about N% (computed). Check that "about doubled" still fits the new staff line (`sp_staff`) each update.
- **Landing page labels.** Each card says "Running cost" (building work and wear taken out, comparable) or "Total spent · not running cost" (totals-only places, `operating:false`). Keep a new place's label right; never show a running-cost, day or per-resident figure for a totals-only place. Dollars carry their country in `currency` in `place.json` (`US$`, `CA$`, `AU$`, `NZ$`, each followed by a non-breaking space), so every figure, in cards, charts and screenshots, says which dollar; use the same for a new place. Website and source are on each report's top line (`about()` in `build.py`), not on the cards.

