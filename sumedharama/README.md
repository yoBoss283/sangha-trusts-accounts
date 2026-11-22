# Sumedharama (Budismo Theravada da Floresta, Portugal): accounts statistics

A one-page, plain-language report of what it costs to run the monastery, from the community's own two-page
"Report to Abbots 2012–2026", shared by Ajahn Vajiro on 17 November 2026 (`report.pdf`: detailed expenses and a balance sheet, years to 31 December). **All amounts are in
euros, as in the report; nothing is converted.** It is not a set of filed annual accounts and has no income statement.
Part of the landing page https://yoboss283.github.io/sangha-trusts-accounts/ (the overview folder builds the card).

- `extract_report.py`: reads the two pages into `raw_expenses.json` and `raw_balance.json` (each number placed in its year by its position).
- `make_data.py`: merges the rows, checks the lines against the report's own totals (it prints the three differences: 2015 €6,360,
  2017 €3.80, 2025 €120.93), works out building additions and "money given", and writes `data.json`.
- `cpi.py`: Portugal's HICP (Eurostat `prc_hicp_aind`: all items and electricity, gas and other fuels), calendar-year averages.
- `people.py`: residents from the Sangha community lists, section "Sumedharama" (yearly totals only, in `people.json`).
- `build.py`: fills `template.html` (copied from the Hartridge page) into `sumedharama-accounts.html` and `-page.html`.

Running costs = the report's total, without depreciation and write-offs, building-project costs listed as expenses (survey,
architects, engineers, project legal costs, shelters, clearing land, project tools, tax on buying land) and interest received.
The notes in the page list each rule. Open questions for the owner: the three small gaps above, and whether the report's
2015 total includes €6,360 of something not listed.


## Source (updated 17 Nov 2026)

2012-2024 come from the community's accounts spreadsheet (read once by `read_spreadsheet.py` into `spreadsheet.json`; the spreadsheet itself is not kept here);
2025 comes from the two-page report (`report.pdf`). `make_data.py` merges them, and writes `footnotes.json`: a lettered footnote for every
place where the page uses a different number from the one posted (the page prints them under the all-figures table). Check list sent back to the
community: `Sumedharama accounts - checks for Ajahn Vajiro.xlsx`.


## Annual accounts check (22 Nov 2026)

The community shared its annual accounts for 2014 to 2024 (balance sheet and profit and loss; scans for some years). The figures are in `filed_accounts.json` (the PDFs are not kept in the repo); `check_filed.py` compares them with `data.json`. Result: the spreadsheet agrees within a euro or two, except 2018 (costs €80.60 higher in the accounts) and 2020 (€40.00 higher), which `make_data.py` now takes from the accounts (footnote g), and 2022 (the accounts show €1,868.68 more cost because €1,867.68 of other income is a separate line; the page keeps the spreadsheet; open question for the abbot). There are no accounts for 2012, 2013 or 2025. The 2012–13 rent is settled (22 Nov 2026): the community confirms the spreadsheet's €15,000 (2012) and €14,500 (2013): about ten months at about €2,500 from June 2012 to February/March 2013 over two accounting years, then €500 a month after the move to Pinhal de Frades, paid until 2018.
