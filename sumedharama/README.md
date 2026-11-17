# Sumedharama (Budismo Theravada da Floresta, Portugal): accounts statistics

A one-page, plain-language report of what it costs to run the monastery, from the community's own two-page
"Report to Abbots 2012–2026" (`report.pdf`: detailed expenses and a balance sheet, years to 31 December). **All amounts are in
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
