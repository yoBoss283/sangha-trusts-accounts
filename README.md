# What it costs to run the monasteries

Plain-language reports on what it costs to run seventeen Theravada forest monasteries (sixteen sets of accounts), and whether
those costs have risen faster than prices in general.

- **The site:** https://yoboss283.github.io/sangha-trusts-accounts/ (the landing page; one card for each place, each
  linking to its full report).
- **Dates:** started 16 November 2026; the four reports were merged into this one repository on 17 November 2026.
- **This repository** is the only copy of the code and data. It is public so that anyone can check the figures.

## What is in it

| Folder | Monastery | Trust | Source | Currency |
|---|---|---|---|---|
| `est/` | Amaravati and Chithurst | English Sangha Trust (charity 231310) | annual accounts 1995–2026, filed at Companies House and the Charity Commission | £ |
| `aruna-ratanagiri/` | Aruna Ratanagiri, Harnham | Harnham Buddhist Monastery Trust (charity 1126476) | annual accounts | £ |
| `hartridge/` | Hartridge, Devon | Hartridge Buddhist Monastery Trust (charity 1142439) | annual accounts 2011–2025 | £ |
| `sumedharama/` | Sumedharama, Portugal | the community (not a filed trust) | its own two-page "Report to Abbots 2012–2026", shared by Ajahn Vajiro on 17 Nov 2026 | € (never converted) |
| `abhayagiri/` | Abhayagiri, California | Sanghapala Foundation (US tax no. 94-3212705) | the yearly tax returns (Form 990), 2011–2023, from ProPublica | US $ (never converted) |
| `tisarana/` | Tisarana, Ontario | Tisarana Buddhist Monastery | the monastery's own financial statements, 2016–2025 | Canadian $ (never converted) |
| `bodhinyanarama/` | Bodhinyanarama, Wellington | Wellington Theravada Buddhist Association (CC29078) | the NZ Charities Register: income and expenditure, years to March 2017–2026 | NZ $ (never converted) |
| `bodhivana/` | Bodhivana, East Warburton VIC | Victoria Sangha Association Inc. (ABN 59 019 586 160) | the ACNC's yearly statements, 2016–2024 | Australian $ |
| `pacific-hermitage/` | Pacific Hermitage, White Salmon WA | Sanghata Foundation (US tax no. 27-2787286) | the yearly tax returns (Form 990), 2011–2023, from ProPublica | US $ |
| `milntuim/` | Milntuim, Glen Artney, Scotland | Milntuim Hermitage Trust (SC043482) | the Scottish Charity Register: income and expenditure, 2020–2025 | £ |
| `temple-forest/` | Temple Forest, Temple NH | Jeta Grove Foundation Inc. (US tax no. 30-0754003) | the yearly tax returns (Form 990), 2014–2020, from ProPublica | US $ |
| `forest-hermitage/` | Forest Hermitage, Lower Fulbrook, Warwickshire | The Forest Hermitage Trust (charity 1173083) | the Charity Commission register: income and expenditure, years to March 2021–2025 | £ |
| `wat-buddha-dhamma/` | Wat Buddha Dhamma, Wisemans Ferry NSW | Wat Buddha Dhamma Foundation Ltd (ABN 41 081 615 992) | the ACNC's yearly statements, 2017–2024 | Australian $ |
| `vimokkharam/` | Vimokkharam, Olinda VIC | Vimokkharam Forest Hermitage Inc (ABN 73 051 793 658) | same | Australian $ |
| `bodhipala/` | Bodhipala, Mount Pleasant SA | Bodhipala Monastery Ltd (ABN 76 627 533 475) | same, 2019–2024 | Australian $ |
| `dhammagiri/` | Dhammagiri, Kholo QLD | Brisbane Buddhist Vihara (Temple) Inc. (ABN 84 358 631 510) | same, 2017–2024 | Australian $ |

The last twelve give totals only (money in, spending and, for some, what they hold), so their pages are shorter. They are built
by `simple_build.py` from `simple/template.html`, with each folder's `place.json` and `data.json`.

The Sumedharama report is not a set of filed accounts: it has detailed expenses and a balance sheet, but no income
statement. Its page says so.

## The ideas behind every page

- **Running costs** means what a place spends in a year to keep going: all spending, without new building work and
  without depreciation (wear on buildings, which is not money paid out). Each trust lists some building costs inside its
  spending (for example plan fees, loan interest on a building, project costs), and these are taken out too. The exact
  rule for each trust is in `RUN` in `build.py`, and each report's notes list what was removed.
- **After inflation.** Money from different years is put into today's prices with the official consumer price index
  (UK: ONS CPI; Portugal: Eurostat HICP). Headline comparisons use three-year averages, never a single year, so one odd
  year does not decide the answer.
- **Residents** are counted from the community lists, as yearly totals only. No names, and no per-person figures are
  presented as a measure of cost.
- **Reserves.** Where the accounts allow it, the page shows how many years of running costs the general reserve would
  cover, next to income and spending.
- **Own words.** Each trust's cost lines are called what that trust calls them (for example "Repairs and upkeep"), not
  one common label.
- **No ranking.** The places are shown side by side, not compared or scored, and the pages state facts without telling
  the reader what to conclude.
- **Nothing typed in by hand** except in each folder's `corrections.txt` / `read_by_hand.txt`, with the reason. Each
  build stops if a year's totals do not add up.

## How it is built

1. Each folder reads its source documents (PDFs, scans, or the spreadsheet) into `data.json`: every figure by year. Scans
   are read with the Mac's own text recognition and then checked; figures that cannot be read for sure go to the owner
   first.
2. Each folder's `build.py` fills its `template.html` and writes the report (`*-accounts.html`, which works on its own
   offline, and `*-accounts-page.html`, the same without the outer page).
3. The top-level `build.py` reads every folder's `data.json`, `people.json` and `cpi.json`, works out the card figures
   (running costs a day, change after inflation, residents, building spend) and writes `index.html` and `pages/*.html`.
   Every number and sentence on the cards is computed, none is typed.

```sh
sh build_all.sh                      # rebuild every report from its saved data, then the landing page
cd est && sh build.sh                # rebuild one place from its source documents (see its README.md)
python3 -m venv venv && venv/bin/pip install -r est/requirements.txt   # only if the PDFs must be read again
```

`index.html` and `pages/*.html` are the built site; GitHub Pages serves them straight from `main`. The "Updated" stamp
in the small print is written at build time, so rebuild before pushing.

Each folder has its own `README.md` with its source documents, scripts and checks. The owner's rules and the history of
decisions are in `REVIEW.md` (review rounds between the reviewing and building sessions) and, for the English Sangha
Trust, `est/REVIEW.md`, `est/BRIEF.md` and `est/HANDOVER.md`.

## Limits worth knowing

- Accounts are annual and group-level; they cannot say what any single item bought, and they say nothing about guests,
  retreatants or lay residents beyond what the notes give.
- Hartridge and Aruna Ratanagiri are lightly maintained; the English Sangha Trust page is the most detailed.
- Sumedharama's "money given" is worked out (net result plus spending), includes building gifts, and is marked as an
  estimate.
- The residents' counts come from a separate private project; only the yearly totals (`people.json`) are kept here.

## Updating when new accounts come out

See `UPDATE.md`. Before an update, `python3 archive.py` keeps a copy of the current site in `archive/`; the landing page then links to it under "Earlier versions". `python3 status.py` shows, for each place, the latest year saved and what is missing. The owner only has to say:
"Check the repo and update it with any new annual reports, follow UPDATE.md."

## History

On 17 Nov 2026 four separate repositories and a Claude page were merged into this one repository and one site. The old
repositories are retired.
