# What this project is trying to show (brief for reviewers)

## The aim

The English Sangha Trust is the UK charity that owns and runs two Buddhist monasteries: Amaravati (Hertfordshire)
and Cittaviveka (Chithurst, West Sussex). Since 2019 it has spent tens of millions of pounds on new buildings,
paid for by very large gifts.

The owner of this project wants to show, in plain charts that people who don't read accounts can follow, that
**the cost of running the monasteries has risen faster than inflation, and the new buildings have not brought it down**,
honestly: if a number doesn't support the case, the page says so (as it does for heating). A common view is that new buildings save money;
the owner's concern is that each new building also brings more heating, electricity, insurance and upkeep, so the
running costs keep climbing.

Building work itself is always left out: it is a one-off, and the accounts count it as something the Trust owns.
"Running costs" here means everything the Trust spends in a year except building work and depreciation.

## Where the figures come from

- The Trust's annual reports and accounts, all public: the Charity Commission register (charity 231310, last five years)
  and Companies House (company 00565499, every year since 1995). All 32 reports are in `accounts/`.
- Older reports are scans; their figures were read by eye (`read_by_hand.txt`) and every year was checked: parts add up
  to totals, and each year's funds follow from the year before. Ten doubtful figures were confirmed by the owner.
- Residents: the number of monks, nuns, novices and anagārikas at the two monasteries, from the monasteries'
  community lists (Vassa list in July, Winter list in January), averaged per April–March year. Lay residents and guests
  are not counted. Nothing is shown per person (the costs also serve guests and retreatants).
- Inflation: the UK consumer prices index (ONS, CPI). Energy prices: CPI 04.5, electricity, gas and other fuels.
  Both averaged April–March (`cpi.py`).
- The page covers the years to March 2002–2026 (the first year with complete resident counts).

## Main findings (as on the page, 16 Nov 2026, after review rounds 1–3)

"Running costs" leave out building work, wear on buildings (depreciation) and a few building costs the accounts count
as spending (planning fees, building-loan interest, the one-off Temple heating replacement). The headline also leaves
out **welfare and food**, shown apart: it includes the care of ageing monks and nuns; the accounts give it as one line.

**Before and after the building programme (2016–18 average against 2024–26, in 2026 prices):**

| | Change |
|---|---|
| Spent on new buildings, 2019–2026 | about £20.5m (buildings owned 4.1 times) |
| Running costs without welfare and food | +£141k a year (+22%) |
| of which staff, office and the rest | +£73k (staff went from 3 to 4 in 2025) |
| heat, light, water and council tax | +£50k (followed energy prices) |
| insurance | +£29k (+69%) |
| travel | +£16k |
| maintenance | −£26k |
| Welfare and food (shown apart) | +£76k (+59%) |
| Wear on buildings (not paid out) | +£346k |
| Residents | 51 → 63 |

- **Heating follows energy prices.** Against the UK household energy price index (ONS CPI 04.5) the bill rose +4%
  since 2016–18 and −17% since 2019–21, while the buildings grew. The page says so plainly, beside the Trust's own
  Passivhaus quote.
- With the same number of residents (2019–21, 61, against 2024–26, 63), running costs without welfare rose 11% after inflation.
- The result depends on the starting year (+9% to +78%); the notes give a table.
- Per pound of buildings, heat, insurance and maintenance fell from 5.6p to 2.0p a year, but there are 4.1 times as many pounds.
- Interest (£182k in 2026, 20% of what the everyday account paid out) comes mostly from the cash held for building, and
  will fall as it is spent.
- About £23k–51k a year of staff cost is counted as building work; it moves into running costs when the programme ends
  unless the posts end.
- The Sala was finished in December 2024, so its full costs are not in the data yet; section 4 gives a five-year estimate as a range.

## How the page is built now

- **Top:** a neutral headline, tiles, a chart of what went up and what went down, running costs plus wear on buildings
  in five-year blocks against inflation, heating against inflation and energy prices, and "What this means" (the only
  place with conclusions).
- **1 The costs in detail:** fixed and variable costs; fixed costs, with the per-pound line; each kind of cost against
  inflation; wear on buildings, with the accounts' rates.
- **2 What the money goes on, and who lives there.** **3 Income, funds and reserves,** with interest shown apart.
- **4 The next five years** (estimate, with the staff point) and **5 Notes**, with the other-starting-years table.

## What feedback is wanted

Is the case convincing? What would a sceptical trustee or supporter say against it? Which charts or numbers make the
point most clearly, and which should go? Is anything unfair or misleading?

## Files

- `est-accounts.html`: the page itself (open in any browser). `template.html` + `build.py`: how it is built.
- `data.json`: every figure per year. `read_by_hand.txt`, `corrections.txt`: figures read or corrected by hand, with reasons.
- `README.md`: the pipeline. `figures.py`: reads the reports and checks the totals.
