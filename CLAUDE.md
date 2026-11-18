# Monastery accounts statistics: notes for Claude (or any AI)

One repo, one site: https://yoboss283.github.io/sangha-trusts-accounts/ . Start with `README.md`.

- **To update for new annual reports, follow `UPDATE.md`.** Run `python3 status.py` first: it shows what is already done.
- Each place has its own folder with its own `README.md` (and, for the English Sangha Trust, `CLAUDE.md`, `HANDOVER.md`,
  `REVIEW.md`). `REVIEW.md` here is the history of review rounds and decisions.
- **Before an update, run `python3 archive.py`** (saves the current site to `archive/<year-month>/`, linked from the landing page under "Earlier versions"). Never edit or delete old copies.
- **Talk before adding features.** Propose a new chart, agree on it, then build it.
- **Plain language**: short sentences, no statistics jargon. Each trust's own cost-line names ("Repairs and upkeep"), not one
  common label. State facts; do not state conclusions outright ("the accounts do not show a saving", not "the buildings did not help").
- **Never guess a figure.** Anything not readable for sure on a scan goes to the owner first, with the PDF page.
- **Read the built page after every change**, including at phone width (375 px, no sideways scroll, text at least 12 px).
- **Privacy:** the owner's real name and e-mail never go in this repo or in commits (commit as `yoBoss283`, no-reply address).
  No names of residents; only yearly totals. The Sangha statistics project (lists, entries) stays separate and private.
- **Do not delete or publish elsewhere:** this is the only repo and site. Old separate repos were retired on 17 Nov 2026.
- Pull and push from the Terminal panel (GitHub login is in the keychain). Ask the owner before pushing and before downloading files.
