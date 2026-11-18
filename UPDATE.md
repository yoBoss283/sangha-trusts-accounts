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
