# Sceptic's review of the EST accounts page

A back-and-forth file. The reviewer writes points; whoever works on the page answers under each **Reply:** line
(what was changed, or why not), and the reviewer reads the replies and adds a new round at the bottom.
Don't delete earlier rounds.

## Round 1 (reviewer, 16 Nov 2026)

Reviewed: the live page (version of 16 Nov 2026, 13:56 GMT), `template.html`, `data.json`, `people.json`, `cpi.json`,
`BRIEF.md`. All numbers below were recomputed from `data.json` and are in 2026 pounds unless they say otherwise.

### The owner's aim, as I understand it

Think like a financial analyst looking at a company that says: "we invested, our buildings are better, we used to pay
so much for maintenance, now it is lower." The analyst asks: **show me where the cost base went down.** The owner
believes it didn't: costs rose almost everywhere, by more than inflation, because more was added. The page should lay
the evidence out so readers reach that conclusion themselves, without the page telling them what to think.

### Verdict in one paragraph

The data is not fake: it traces to the published accounts, and the sums check. But **the page does not yet prove the
point, and in places its own numbers argue against it.** The headline leads with the cost lines that are weakest for
the case (heating, insurance, maintenance together +13% while the buildings grew fourfold, which a trustee will read as
"the new buildings are cheap to run"), and leaves out of the main story the two things that make the case strongest:
**wear on buildings** (the real long-run cost of owning more) and **the interest income that disappears when the cash
is built with.** It also uses wording ("did not", "have not brought these costs down") that tells the reader the
conclusion instead of letting them reach it.

### What a sceptical trustee would say, point by point

**1. "You left out the biggest cost of the buildings."**
Running costs exclude depreciation. Fair as cash, but depreciation is exactly the "long run" the owner is talking
about. From 2016–18 to 2024–26 (2026 £, a year): cash running costs +£216k (+28%); wear on buildings **+£346k
(+220%)**; the two together +£562k (**+61%**). And £298k a year of the wear (2026) is on fittings, plant, equipment and
vehicles that last 5–10 years: that is real cash coming back round soon, not a paper figure. Right now it is a
footnote card in section 1.
- Suggestion: one main chart, "what it costs to own and run the places": cash running costs plus wear, stacked, against
  inflation. Say plainly that wear is not cash paid this year but what replacement will need.

**Reply:** Figures checked against `data.json`: wear +£346k a year, cash running costs +£216k, matching. Agree it is the
strongest long-run point, and the £298k a year on 5–10-year items is real cash coming round. Not built yet: a new main chart
("to own and run the places": running costs plus wear, against inflation) changes the top of the page, so it goes to the
owner first. Note for the wording if it goes ahead: wear is the accountants' write-off of past spending, so it must be
labelled "not paid this year", and wear before 2000 is not comparable (buildings were not written down then).
**2. "Show me the savings." (the analyst's question, not yet answered)**
The page never sets the saving next to the cost. A cost bridge does it in one picture. 2016–18 → 2024–26, a year, 2026 £:

| Line | Change a year |
|---|---|
| Maintenance (the only line that fell) | **−£26k** |
| Heat, light, water and council tax | +£50k |
| Insurance | +£29k |
| Travel | +£16k |
| Everything else (staff, office, equipment, books, fees) | +£73k |
| Welfare and food | +£76k |
| **Cash running costs** | **+£216k** |
| Wear on buildings | +£346k |
| **Cash running costs and wear** | **+£562k** |

Against roughly £17.5m spent on building work from 2019 to 2026, the one saving is about £26k a year: 0.15% of the
money spent. A reader who sees that table needs no adjective.
- Suggestion: make this bridge (a waterfall chart, maintenance as the single bar going down) the first chart.

**Reply:** Bridge recomputed: −£26k maintenance, +£50k heat, +£29k insurance, +£16k travel, +£73k everything else, +£76k
welfare and food, +£216k cash, +£346k wear: all match. One correction: building spending 2019–2026 was about £20.5m, not
£17.5m; the yearly data has capital spending only from 2020 (£17.5m), and the 2019 trustees' report gives £3.0m for that
year. So the single saving is about 0.13% of the money spent, not 0.15%. Agree this is the clearest picture. Proposed to the
owner as the first chart; not built yet (headline change).
**3. "More people live there, so of course it costs more."**
Residents rose 24% (50 → 62) between the two periods the headline compares, and the page no longer shows that next to
the headline. That is the first thing a trustee will say. There is a cleaner comparison in the data: **2019–21 against
2024–26, when the number of residents barely changed (+3%)**. Over that span cash running costs rose 19% after
inflation, insurance +48%, welfare and food +68%, heat +11%, maintenance −10%.
- Suggestion: use this "same number of people" comparison somewhere prominent, or show the residents next to the
  headline. Hiding the confounder makes the page easier to dismiss.

**Reply:** Agree. Checked: 2019–21 → 2024–26 residents +3%, cash running costs +19%, insurance +48%, welfare and food +68%,
heat +11%, maintenance −10% after inflation. The page has this comparison only inside the heating caption. Proposed to the
owner: show residents next to the headline numbers, and give the "same number of people" comparison its own line under
them. Not built yet.
**4. "You picked the starting point."**
The headline (+22% for running costs without welfare) moves a lot with the base years:

| Base → end | Running costs without welfare, after inflation |
|---|---|
| 2016–18 → 2024–26 (the page) | +22% |
| 2017–19 → 2024–26 | +13% |
| 2013–15 → 2024–26 | +19% |
| 2016–18 → 2021–23 | +9% |
| 2017–19 → 2021–23 | 0% |

Almost all of the rise is in the last three years. That fits the owner's story (the newest buildings came into use)
but also fits staff (about £57k in 2024 → £106k in 2025), the Retreat Centre reopening in 2025, and the energy price
shock. A small "the result with other starting years" table answers the cherry-picking charge before it is made.
- Also: the page says "since the building programme began in 2019", but in the code that year is the year the
  resident count settled near 60 (`template.html` line 531), not a building date. Buildings already rose from £4.7m
  (2016) to £5.5m (2017). Tie the label to the building dates in the accounts.

**Reply:** Agree on both. (a) The starting-year table: proposed to the owner as a small table in the notes or under the
headline; not built yet. Earlier the owner chose not to start in 2011 because it weakens the case, so this table would show
that openly too, which is the point. (b) Fixed: the year is now a constant `BUILD_START = '2019'` in `template.html`, with
the reason from the accounts (the 2019 trustees' report: £3.0m of capital spending, Heartwood House bought, the nuns'
buildings and the Bhikkhu Vihara designed), used for the headline, the chart marker, the before/after base and the
estimate. The resident-count year is now used only where the text is about residents. Output unchanged (both are 2019).
Building spending was already £924k in 2017, so "began" is arguable; the notes could say "the large building programme".
**5. "Energy prices went through the roof; that's not us."**
Heating and power is compared with general inflation (CPI). UK gas and electricity prices rose far faster than CPI in
2022–23, so part of the +44% is prices, not more building. The caption admits this, but the headline tile does not.
- Suggestion: deflate heat by the ONS energy price index (CPI household energy, or the non-domestic energy series) as
  well. If heat still rose faster than energy prices, that is real extra use, and much stronger evidence. If it didn't,
  better to know now.
- Same for insurance: commercial property premiums rose across the UK. And insurance grew +69% while the buildings
  insured grew about fourfold, so per pound insured it fell. A trustee will spot this.

**Reply:** Agree this is the test that decides how strong the heating claim is. Not done yet: it needs the ONS energy
series (CPI electricity, gas and other fuels, or a non-domestic series) downloaded into the repo and averaged per
April–March year like `cpi.py`. I'll propose it to the owner as analysis first, result reported before anything goes on
the page. Insurance per pound insured: agree, it fell (point 6); see there.
**6. "Per pound of building, it has never been cheaper to run."**
Heat, insurance and maintenance as a share of the buildings' book value: about 5.6% a year in 2016–18, **1.9% in
2026**. This is the strongest counter-argument, and it comes straight from the page's own figures. The owner's answer
is probably: "cheaper per pound, but there are far more pounds, and the total only goes up." The page should face this
openly, e.g. one line: "Each pound of building costs less to run than before, but there are four times as many pounds
of building, so the bill still grows."

**Reply:** Agree, and the owner's own answer fits ("cheaper per pound, but four times the pounds"). Proposed to the owner:
one plain line next to the fixed-costs chart with both numbers (5.6% → 1.9% of book value; total still up). Not built yet.
**7. "The cash in the bank is paying for this, and it won't last."**
Not on the page as an argument, and it is one of the best for the owner. Interest on free (unrestricted) money was
about £4k in 2020, £316k in 2024, £181k in 2025 and £182k in 2026: in 2026 that is roughly a fifth of what the
everyday account spent. That interest comes from cash waiting to be built with. Once it is spent on buildings, the
interest goes and the buildings' costs arrive. That is the classic analyst point: **the investment both removes income
and adds cost.**
- Suggestion: show everyday income with and without interest, against running costs and wear. Check first which cash
  earns which interest (restricted vs general), from the notes to the accounts.

**Reply:** Checked: unrestricted interest £3.5k (2020), £316k (2024), £181k (2025), £182k (2026). The 2026 report's note
3 splits it: £182k unrestricted, £81k restricted (of £263k), and the 2026 cash (£11.4m) is mostly the new £9.5m building
gift, so the unrestricted interest will fall as that is spent. Agree it is a strong, fair point. The everyday-account chart
used to show interest and legacies apart; for 2020–2026 that split exists, before 2020 it does not. Proposed to the owner;
not built yet.
**8. "Welfare and food has nothing to do with buildings."**
The page already shows it apart, which is right. But it says it is "mostly the care of an ageing community"; the
accounts don't split it, and an earlier note says only the treasurer can break it down. Unless that is confirmed,
"mostly" is a claim the page can't back. Say "includes" instead.

**Reply:** Partly agree. "Mostly" comes from the owner, who knows the community, not from the accounts. The page backs it
with the senior monks and nuns count (4 → 13 with 20+ years in robes, under the welfare chart) and the funds the reports
name (the senior monk's welfare fund, the Samana Care Fund, the Ageing Samanas Fund). I'll ask the owner whether to keep
"mostly" with "(the community's own account)" or change to "includes". Not changed yet.
**9. "Did anyone actually say the new buildings would save money?"**
The thesis answers a claim ("new buildings will be cheaper to run"). If the trustees' reports say that, quote them
(year and page), then show the numbers under the quote: that is the most persuasive layout there is, and it lets
readers judge. If nobody claimed it, the page risks arguing with a position no one holds; then frame it as "what did
the investment do to the cost of running the places?"

**Reply:** Checked the 2014–2026 reports. Nobody promises lower running costs. What they do say: 2022, "The Sangha and Trust
agreed on a passive house/energy-efficient design" (Sala, kitchen and work-yard); 2025 and 2026, "New buildings are being
constructed in accordance with very progressive Passivhaus standards of energy efficiency, including high levels of
insulation, solar collectors where possible, heat pumps and all-electric kitchens." So the fair framing is the second one:
"what did the investment do to the cost of running the places?", with the Passivhaus quote above the heating chart and the
numbers under it. Proposed to the owner; not built yet.
**10. Tone: let the numbers speak.**
The owner wants readers to draw the conclusion. Right now the hero sentence does it for them in bold ("The new
buildings have not brought these costs down", "did not: they rose"). Sceptical readers push back against a page that
argues; they trust a page that shows. Suggest: neutral headings ("What changed between 2016–18 and 2024–26"), the
bridge table, and let the red bars do the talking. Keep the conclusions to the "What this means" box, worded as
findings, not verdicts.

**Reply:** Agree in principle; it is the owner's call, since the hero wording was written at their request. I'll propose
neutral headings ("What changed between 2016–18 and 2024–26") with the verdict sentences moved into "What this means" as
findings. Not changed yet.
**11. Smaller things**
- `BRIEF.md` is out of date: it still describes per-person headlines and "+3% per person", which the page dropped.
  Outside reviewers will be confused.
- The latest-year tile showing buildings "4.1×" next to "+13%" for building-linked costs undercuts the message on its own.
  Either explain it (point 6) or don't put them side by side.
- The Sala finished December 2024, so only about 15 months of its costs are in. Section 4's estimate range is the
  right way to handle it; mention this next to the headline too.

**Reply:** `BRIEF.md` updated to the current page (no per-person figures, five-year blocks, welfare shown apart, what each
section holds). The "4.1×" tile next to "+13%": to be settled with point 6 (explain it, or move the buildings tile).
The Sala's 15 months: proposed to the owner as a short note next to the headline; the hero already says "the newest
buildings are not yet fully in these figures".
### What would make the case convincing (summary)

1. First chart: the cost bridge (point 2). Savings vs added costs, one picture.
2. Second chart: cash running costs plus wear, against inflation (point 1).
3. A "same number of people" comparison (point 3) and a starting-year check (point 4).
4. Heat against energy prices, not only CPI (point 5).
5. The interest income that will disappear (point 7).
6. Neutral wording; the trustees' own words, if they promised savings (points 9, 10).

If after points 1, 2, 5 and 7 the numbers still point the owner's way, the case is solid. If heat turns out to track
energy prices and the cost bridge is mostly welfare and staff, the honest conclusion is narrower: "the investment did
not lower costs", not "the buildings drove costs up". That is still worth showing.

## Round 2 (reviewer, 16 Nov 2026)

Round 1 replies read, and commit 2971c56 checked. The £20.5m correction is accepted (0.13% of the money spent, not 0.15%).
The `BUILD_START` fix and the updated `BRIEF.md` are good.

### New points

**12. The Passivhaus quote changes what the page has to test.** This is the best find of round 1. The Trust does make a
claim, and it is about energy: "very progressive Passivhaus standards of energy efficiency ... heat pumps and all-electric
kitchens". So the heating chart *is* the test of the Trust's own claim, and the energy-price check (point 5) should come
**before** any page changes, because it decides how strong the case is. Three cautions for that check:
- The accounts line is "heat, light, water **and council tax**". Water and council tax don't follow energy prices.
  If any year's report splits the line (or the notes give council tax), use it; if not, say the check is rough.
- Heat pumps and all-electric kitchens move spending from gas to electricity, and electricity prices moved differently
  from gas. Use the combined energy series (ONS CPI 04.5, "electricity, gas and other fuels"), averaged April–March like
  `cpi.py`.
- Report the result here as it comes out, before anything goes on the page: "heat rose X% more (or less) than energy
  prices".

**Reply:** Done, analysis only, nothing on the page yet. Series added to the repo: ONS CPI 04.5 "electricity, gas and other
fuels" (D7CH, `ons_energy_d7ch.csv`) and CPI 04.5.1 electricity (D7DT, `ons_electricity_d7dt.csv`), averaged April–March
like `cpi.py`. Result for the "heat, light, water and council tax" line (averages of three years):

| Period | Bill as paid | General prices (CPI) | Energy prices (04.5) | Electricity (04.5.1) | Bill beyond energy prices |
|---|---|---|---|---|---|
| 2016–18 → 2024–26 | +91% | +33% | +83% | +94% | **+4%** |
| 2019–21 → 2024–26 | +39% | +25% | +68% | +63% | **−17%** |
| 2002–04 → 2024–26 | +388% | +81% | +370% | +366% | **+4%** |

So the bill has tracked UK energy prices almost exactly over twenty years, and since 2019 it rose *less* than energy prices
while the buildings grew about fourfold. Read plainly, energy use has not risen with the buildings, which is what the
Trust's Passivhaus claim would predict. The "+44% after inflation" on the page is energy prices, not more use. Cautions,
as you said: water and council tax are in the line (the 2002–03 notes split them: water about £4–5k and council tax about
£4k a year, a small part then; no recent split), price contracts can lag the index by a year or two, and the move from gas
to electricity is covered by the combined series. This goes to the owner before any wording changes.
**13. Staff almost doubled in 2025 (£57k → £106k).** That is about a quarter of the whole rise in cash running costs. A
sceptic will ask whether it has anything to do with the buildings: an estates or facilities post would support the
owner's case, an office post would not. Please look at the 2025 report (staff note or trustees' report) and say what
changed. If a new post is linked to the buildings, it belongs in the cost bridge with that label.

**Reply:** From note 10 (staff costs): the average number of staff went from 3 to 4 in 2025, all under "administrative and
project management"; total staff cost £142,642 → £192,643. In both years about £50k of it was counted as building work
("costs directly attributable to the new building programme at Amaravati": £50,982 in 2024, £50,302 in 2025, £22,931 in
2026), so the staff line in running costs rose from £57k to £106k by the cost of the fourth person. The reports don't say
what the new post is; nothing links it to the buildings in writing. So in the bridge it stays "staff", unlabelled. One
related point for the outlook: as the building programme ends, the share of staff cost now counted as building work
(£23k–51k a year) will fall into running costs unless those posts end.
**14. Order of work.** Analysis first (points 5/12 and 13), then the page, because the analysis may change the wording.

**Reply:** Agreed and followed: 5/12 and 13 are done as analysis (above), nothing built. The energy result changes the
heating wording and probably the headline, so it goes to the owner first, together with your D1–D11.
### Decisions for the owner (not yet answered)

The owner answers each line with yes, no or a change. The reviewer's recommendation is in the last column. Nothing on
this list should be built until the owner has answered it.

| # | Proposal | Recommendation |
|---|---|---|
| D1 | Cost bridge as the first chart: what went down (maintenance) against what went up, 2016–18 → 2024–26 | yes |
| D2 | Main chart "running costs plus wear on buildings", against inflation, with wear labelled as not cash paid this year | yes |
| D3 | Residents shown next to the headline, plus one line for 2019–21 → 2024–26, when residents barely changed | yes |
| D4 | Small table "the result with other starting years" (in the notes) | yes |
| D5 | Heating checked against energy prices (analysis first, reported here before anything goes on the page) | yes |
| D6 | One line by the fixed-costs chart: cheaper per pound of building (5.6% → 1.9%), but four times the pounds | yes |
| D7 | Chart of everyday income with and without interest, and a note that the interest falls as the building gift is spent | yes |
| D8 | Welfare and food: "mostly the care of an ageing community" → "includes the care of …" | yes ("includes") |
| D9 | The Trust's Passivhaus quote above the heating chart, numbers underneath | yes, after D5 |
| D10 | Neutral headings and hero ("What changed between 2016–18 and 2024–26"); verdicts only in "What this means", as findings | yes |
| D11 | Short note by the headline: the Sala's full costs are not in yet (finished Dec 2024) | yes |

Owner's answers (16 Nov 2026, given in the reviewer's session): **all of D1–D11 approved as recommended**, and the
"when to stop" rule below is accepted.

### When to stop (accepted by the owner, 16 Nov 2026)

The owner wants the rounds to stop when the page is good enough, not to go on forever. Proposed meaning of "good enough":
1. Every decision above is built, or dropped by the owner.
2. The energy-price check (D5) and the staff question (point 13) are answered, and the wording matches what they found.
3. A sceptical reader can find each obvious objection (more residents, energy prices, starting year, cost per pound of
   building, welfare) answered on the page itself.
4. The reviewer has no point left that would change a number or a conclusion. Points about wording only don't hold it up.

Publishing (the live Claude page, the password-locked GitHub page) stays with the owner, as before.

## Round 3 (reviewer, 16 Nov 2026)

Round 2 replies and commit e101f5e read. Both analyses are clear and well done. The owner has approved D1–D11, so the
page can now be built. What the energy result means for that build:

**15. Heating can no longer lead.** The heating bill followed UK energy prices (+4% beyond them since 2016–18, −17% since
2019–21). Showing "+44% after inflation" as a cost of the buildings would now be misleading, and a trustee with the ONS
series would take the page apart with it. So:
- The heating tile goes from the headline. The heating chart stays, with a second dashed line for energy prices.
- D9 is still built, but honestly: the Trust's Passivhaus quote, then "the bill has followed energy prices; it has not
  risen with the buildings". That is a fair point in the Trust's favour, and showing it makes the rest of the page more
  credible.
- The case now rests on what the energy check doesn't touch: the cost bridge (D1: one saving of £26k a year against
  +£216k), wear on buildings (D2: +£346k a year), insurance (+69%, in a market that also rose: say so), the interest that
  disappears (D7), and the total.

**Reply:** Done (adc3b23): the heating tile is gone; the heating chart has an energy-price mark (and since round 4, no general-inflation mark); the Passivhaus quote sits above it with "The bill rose with UK energy prices, not with the buildings". The top now rests on the bridge, wear, insurance, interest and the total.
**16. The staff point you found belongs in the outlook.** £23k–51k a year of staff cost is now counted as building work.
When the programme ends, that moves into running costs unless the posts end. Add it to section 4's estimate as one
listed assumption, and to the bridge's footnote. It is exactly the "the cost doesn't go away, it moves" point the owner
cares about, and it comes straight from note 10.

**Reply:** Done (9e962e4): in the bridge's "How to read this", and as a listed assumption in section 4 (the higher estimate adds about £41k a year, the 2024–26 average, once the building is done).
**17. The headline after the rebuild.** Suggested shape, neutral (D10): "Between 2016–18 and 2024–26 the Trust spent
about £20.5m on buildings. Running costs rose £216k a year after inflation; one cost fell (maintenance, £26k a year). Wear
on the buildings rose £346k a year." Then residents (D3) and the Sala note (D11) right underneath. Check every number
against the rebuilt page before it goes in.

**Reply:** Done, with +£141k (without welfare) instead of +£216k, as agreed; numbers checked against the built page.
**18. Building order (suggested):** D8 and D10 wording first (small); then D1 and D2 (the new top); D3, D4, D6, D11
(lines and notes); D7; heating chart with energy prices plus D9; section 4 with point 16; `BRIEF.md`. Rebuild and read
the page after each step. Message the reviewer when the top of the page (D1, D2, D10) is rebuilt, so it can be checked
before the rest.

**Reply:** Followed in that order; the reviewer was messaged after the top and after the content items.## Round 4 (reviewer, 16 Nov 2026): make it easy to read, above all on a phone

Commit adc3b23 checked. The numbers are right, and the "+£216k" in point 17 was running costs with welfare: the page's
+£141k without welfare is the consistent figure. Content: once D4, D6, D7 and section 4 (with point 16) are built and
`BRIEF.md` is updated, the content side meets the stop rule. The owner's last request (16 Nov, before going to bed) is
to make the page easier to read, in general and above all on a phone. So this round is about reading, not numbers.

Checked in a browser at phone width (375 px, dark mode), with every fold open:

- Good already: nothing scrolls sideways; the side-by-side charts drop to one column below 760 px, so they are not
  squeezed together on a phone.
- **Text inside charts is too small on a phone.** Charts are drawn 600 units wide and shrunk to about 305 px, so
  everything in them is about half size: the smallest chart text is **6.5 px**, the typical **10 px**. The worst: the
  names on the left of the cost bridge, and the "52 residents" lines under the bars.
- **Captions are long:** 78, 69 and 80 words under the main charts, and 156 in "What this means". On a phone each is
  a full screen of grey text.
- **The top sentence holds five numbers in 64 words**, and then the tiles repeat them. With five tiles, the fifth sits
  alone on a phone.
- **The heating chart has two dashed lines** (inflation and energy prices) that look almost the same.
- Hover tips don't work on a phone (no hover), so any number only in a tip is lost there.

### What to change (R1–R10)

**R1. Chart text at least 11 px on screen, value labels 12 px.** Simplest: when the chart is narrower than about 480 px,
draw it with a narrower viewBox (e.g. 360 units, so text is close to its real size), and redraw on resize/rotate.
Check the actual rendered size, as above (`getBoundingClientRect().height` of `svg text`).

**Reply:** Done. Each chart is now drawn at the width it is shown at (its card's width), so text is its real size, and the page redraws when the width changes by more than 30 px (rotation). Chart text is 12 px, value labels 12.5 px. Five-year labels go on two lines ("2002" / "–2006") when bars are narrow. Measured (`getBoundingClientRect` scale × font size): smallest chart text **12.0 px at 375 px and at 320 px**, 11.8 px on a 1024 px desktop (pie labels); nothing scrolls sideways at any of the three.
**R2. The cost bridge as HTML bars, not SVG.** The `.hbars` style already in the page (name, bar, value; on a phone the name
goes above its bar) makes the text real page text, readable at any width. Keep the colours and the order.

**Reply:** Done: the bridge is HTML (`.hbars`), name above its bar on a phone, page text at 14 px. Colours and order kept; a zero line marks where rises start, maintenance goes left.
**R3. Residents under the bars:** too small to read. Put them as one row of plain text under the chart
("Residents: 52 · 57 · 49 · 58 · 63"), or in the caption.

**Reply:** Done: one row of plain text under the chart ("Residents in each five years: 52 · 57 · 49 · 58 · 63"); the same for the senior monks and nuns under the welfare chart. For the running-costs chart they are in its "How to read this".
**R4. Captions: lead with the finding, at most two short sentences.** Everything else (how it's worked out, cautions)
goes in a small "How to read this" fold under the chart. "What this means": at most four short sentences, one idea each.

**Reply:** Done for the three top charts and "What this means": each caption is the finding in two sentences (about 25 words); method and cautions moved into a "How to read this" fold under the chart. "What this means" is four sentences. Section 1–4 subtitles are unchanged (they sit in the detail sections).
**R5. Top of the page:** one or two short sentences (about 30 words), then the tiles. Four tiles, so they pair up on a
phone: running costs +£141k, wear +£346k, insurance +69%, residents +24%. Put "about £20.5m on buildings, 4 times as much
building" in the sentence instead of a tile. The footnote under the tiles: one line.

**Reply:** Done. Top sentence: 36 words, three numbers (£20.5m, £141k, £346k), with "4 times as much" in it. Four tiles, two by two below 760 px: running costs +£141k, wear +£346k, insurance +69%, residents +24%. Footnote: one short paragraph (base years, same-residents +11%, the Sala).
**R6. Heating chart:** make energy prices the one line that stands out (its own colour, labelled at the end of the line:
"energy prices"), and general inflation faint or gone, since the point of this chart is energy.

**Reply:** Done: general inflation is gone from the heating chart; energy prices are the one dark, thicker dashed mark, named in the legend "Energy prices only, from 2002–06". Bar values moved inside the bar tops so the marks don't cover them. Not done: a label at the end of the line (no room at 320 px; the legend says it).
**R7. Chart titles say the finding**, e.g. "One cost fell; the rest rose" rather than "Changes by kind". Short (under 8
words) so they fit on one or two lines on a phone.

**Reply:** Done for the top: "One cost fell; the rest rose", "Running costs and wear outpaced inflation", "Heating followed energy prices". The section 3 interest chart already reads "Interest helps pay the running costs, for now". Detail-section titles unchanged.
**R8. Pies:** five pies in a column are very long on a phone and hard to compare. Show one 100% bar per five-year block
(all five under each other, same order and colours) instead. It is in a folded section, so this is a reading change, not a
change to the top.

**Reply:** Not done, on purpose: the owner asked for pies by name ("the pie chart always works better", names and amounts in the slices), so replacing them is the owner's call. Instead, on a narrow screen each pie is drawn at its shown size (about 300 px) without the labels beside it (the list under each pie gives every kind); text in the pies is now 12.5 px on a phone. Offer to the owner: 100% bars as an alternative.
**R9. Tables:** the year-by-year table is 2,400 px wide; keep it scrolling inside its card, but keep the first column
fixed while scrolling (`position: sticky`) and add "swipe to see more years" above it on narrow screens. Numbers shown only
in hover tips should also be in a label or the caption, or open on tap.

**Reply:** Done: the year-by-year table keeps its first column fixed while scrolling, and "Swipe sideways to see more years." shows above it below 760 px. Tips open on tap (a tap fires the chart's mousemove). The top's numbers that were only in tips are now in labels, captions or the folds.
**R10. Check after each change at 375 px and 320 px wide, light and dark mode, and on a desktop width:** no sideways
scroll, no text under 11 px in charts, nothing overlapping. Note the measured smallest text size in your reply.

**Reply:** Checked in a browser at 375 px (light), 320 px (dark) and 1024 px (light): no sideways scroll; smallest chart text 12.0 px at 375 and 320, 11.8 px at 1024; smallest page text 12 px. Fixed on the way: block labels colliding at 320 px; energy marks covering the heating values; pies at 8 px on desktop; two charts drawn too small for wide cards.
Order: R5 and R7 (wording, quick), R1, R2, R3, R6, R4, R8, R9, R10 at the end. Same rule as before: the owner publishes.

## Round 5 (reviewer, 17 Nov 2026): verdict

Commits 9e962e4 and 2fca534 checked, at 375 px in a browser with every fold open: no sideways scroll; the smallest chart
text is 14 px; four tiles pair up; the top sentence is 36 words; chart titles say the finding; the captions under the
main charts are 20–25 words. The figures in D4, D6, D7 and section 4 match `data.json`.

**The stop rule is met.** Every decision is built (R8 left to the owner, see below), the energy and staff questions are
answered on the page, each obvious objection has its answer on the page, and the reviewer has no point left that would
change a number or a conclusion.

Left for the owner (not blocking):
- R8: keep the pies (their earlier choice) or switch to one 100% bar per five-year block.
- "What this means" is still 91 words; it could be four short sentences. Wording only.
- Publishing: the live Claude page and the password-locked GitHub page are unchanged until the owner says so.
