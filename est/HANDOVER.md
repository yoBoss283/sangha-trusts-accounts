# Handover: monastery accounts statistics pages

Read this first in a new chat. It sums up how the English Sangha Trust (EST) page was made, every rule the owner agreed,
and how to make the same page for the other two UK monasteries: **Aruna Ratanagiri (Harnham)** and **Hartridge**.

## Starter prompt for the new chat

> Read `~/Documents/Sangha accounts statistics/HANDOVER.md`. I want the same accounts statistics page for
> <Aruna Ratanagiri / Hartridge>. Start by finding the charity's annual accounts on the Charity Commission register
> (and Companies House if it is a company), then follow the steps in the handover. Talk to me before adding charts.

## What the EST page is

- One page, plain words, for people who don't read accounts: what it costs to run the monasteries, and whether that
  rose faster than inflation since the building programme began (2019).
- Live: https://yoboss283.github.io/sangha-trusts-accounts/pages/est.html (the old Claude page is deleted).
- Code and data: public GitHub repo https://github.com/yoBoss283/sangha-trusts-accounts, folder `est/`.
- Files: `BRIEF.md` (for outside reviewers), `REVIEW.md` (five review rounds, all decisions), `README.md` (pipeline),
  `CLAUDE.md` (repo rules).

## Pipeline (copy it, change the names)

1. `accounts/`: every annual report PDF, year in the file name. Sources: Charity Commission register (last 5 years,
   the charity's own PDFs) and Companies House filing history (every year since the 1990s, mostly scans).
2. `extract.py`: PDF → `txt/<year>.txt`. Scans have no text: OCR with the Mac's Vision (`ocr.swift`), laid out in columns.
   Encrypted PDFs need `cryptography` for pypdf.
3. `figures.py`: reads the figures, compares the two readings of each year (every report has this year and last year),
   checks that totals add up (funds roll forward, parts = totals, general fund start + in − out + moved + gains = end).
   - Old scans: OCR digits are unreliable (auditors' tick marks over digits). Read the core figures by eye from crops into
     `read_by_hand.txt`, with the page they came from. `corrections.txt` for single fixes, each with a reason.
   - **Ask the owner before filling an unreadable figure**: list the doubtful ones with page numbers; they check.
4. `cpi.py`: ONS CPI (D7BT) and household energy prices (CPI 04.5, D7CH) → April–March averages (`cpi.json`, `energy.json`).
5. `people.py`: residents per Trust year from the Sangha community lists (`../Sangha statistics/entries_fixed.json`):
   bhikkhus, nuns, sāmaṇeras, novices, anagārikas in that monastery's section, average of the Vassa (July) and Winter
   (January) lists. Section names: `Aruna Ratanagiri`, `Hartridge`. **Only yearly totals leave the Sangha repo**, never
   names or entries.
6. `build.py`: fills `template.html` → `*-accounts.html` (works offline) and `*-page.html` (for the artifact).
   `sh build.sh` runs it all and stops if a total doesn't add up.

## Definitions (agreed with the owner)

- **Running costs** = total spending − depreciation − building costs the accounts count as spending (planning fees for
  new buildings, building-loan interest, one-off big replacements like the Temple heating). List each one taken out,
  with amounts, in the notes, plus a table from "total expenditure" to "running costs".
- **Welfare and food** is shown apart in the headline: it includes the care of ageing monks and nuns, not buildings.
  Say "includes", not "mostly".
- **Building spend**: say "new buildings and infrastructure".
- **Never headline** the book value of buildings ("owns 4 times as much") or depreciation ("wear +£346k"): the owner
  calls these accounting figures that mean nothing to readers. Depreciation may stay as an explained detail lower down.
- **Inflation**: CPI averaged April–March. Compare **three-year averages** (one odd year can't swing it). Main charts in
  **five-year blocks** with an inflation mark.
- **Heating**: the accounts line is "heat, light, water and council tax". Check it against the energy price index before
  saying anything. For EST it followed energy prices: the page says the new buildings have not brought the energy bill
  down, and that rising less than energy prices may be the efficient buildings or fixed-price contracts (2023: prices
  nearly doubled, bill didn't move). Never claim energy *use* rose: the accounts show money paid.
- **Staff counted as building work** (staff note): it moves into running costs when building ends. Say so.
- **Interest** on money held for building helps pay running costs now and falls as that money is spent. Show it apart.
- No figures per person/resident: costs also serve guests, retreatants, lay residents. Show residents beside the bars.

## The owner's preferences

- Plain language, short sentences, no statistics words. Graphs over numbers. Charts that say the finding in the title.
- Honest: "if the numbers don't show it, that's it; we don't fake it, but show reasonable trends". When a number goes
  against the case (heating), say it plainly; it makes the rest more credible.
- Never suggest cuts. Use "fixed costs" (come with the buildings: heating, insurance, maintenance) and "variable costs"
  (come with the people: welfare, food, travel).
- Pies for "what the money goes on", names and amounts inside, "Other" last, one pie per five-year block.
- Name the places ("What it costs to run Amaravati and Chithurst"), not "the monasteries" or "the Trust".
- Talk before adding a chart; build after a yes. Read the built page back after every change.
- Must read well on a phone: chart text ≥ 12 px (draw charts at their shown width), captions two sentences with a
  "How to read this" fold, no sideways scroll at 320–375 px.

## Page layout that worked (top to bottom)

1. Title, one or two short sentences (building spend; running costs after inflation; only maintenance fell), four tiles
   (building spend, running costs +£/yr, insurance %, residents %), one-line footnote (base years, same-residents check,
   newest building not fully in).
2. "What it takes to run …": £ a year, a day, a month; then and now in today's money; bars per period with residents.
3. "One cost fell; the rest rose": change per kind of cost a year, after inflation (HTML bars).
4. Running costs against inflation (five-year blocks); heating against energy prices with the Trust's own quote.
5. "What this means": four short sentences, the only place with conclusions.
6. Detail sections: fixed and variable; each kind against inflation; pies; residents; income, funds, reserves, interest;
   a five-year estimate as a range; notes, other-starting-years table, all figures year by year.

## Review process

`BRIEF.md` for an outside AI reviewer; replies under each point in `REVIEW.md`; decisions table for the owner
(yes/no each); stop when every decision is built or dropped and no point would change a number or conclusion.

## For Aruna Ratanagiri and Hartridge: check first

- Find each charity on the Charity Commission register and see whether it is also a company (Companies House filings).
  Note the charity number and the years available.
- Small charities (income under £250k) may file **receipts and payments** accounts: no depreciation, different layout,
  maybe no breakdown of costs. Then the categories must follow what those accounts give; agree them with the owner.
- One trust may run more than one place, or a place may share a trust; check what the accounts cover before comparing
  with residents.
- Big one-off building years and restricted gifts: take building out of running costs the same way, and list it.
- Make it a new repo or a new folder per monastery; keep the same pipeline and template.

## Privacy and publishing

- Public repo: commit as `yoBoss283 <yoBoss283@users.noreply.github.com>`, never the owner's real name or e-mail. Run
  git pull/push in the Terminal panel (keychain login).
- No Sangha data beyond yearly counts; never the "Doris 2007" data.
- Publishing the Claude page only when the owner says so in their own chat (not relayed by another session).
