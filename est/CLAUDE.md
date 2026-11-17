# English Sangha Trust accounts statistics: notes for Claude

Start with `README.md` (pipeline and how to add a year). Same working style as the Sangha community list statistics
(`~/Documents/Sangha statistics`): talk before adding features, plain language, read the built page after every change.

- **Years** are named by the year the accounts end in (31 March): "2025" = April 2024 to March 2025.
- **Group figures only** (the Trust plus Amaravati Developments Ltd), never the company-only columns.
- **Never type a figure in by hand** except in `corrections.txt`, with the reason; `sh build.sh` must say "all add up".
- **Live page:** the combined site, https://yoboss283.github.io/sangha-trusts-accounts/pages/est.html . This folder is `est/` of the
  repo `sangha-trusts-accounts`; rebuild with `sh build.sh`, then `sh ../build_all.sh`.
- **Hand-read figures:** anything that can't be read for sure on a scan goes to the owner first (a check page with the
  scan line), never a guess. Confirmed ones are marked "checked" in `read_by_hand.txt`.
- **GitHub:** public repo https://github.com/yoBoss283/sangha-trusts-accounts (the owner chose public on
  16 Nov 2026, including the yearly resident counts in `people.json`). Commit only with the GitHub no-reply identity:
  `git -c user.name=yoBoss283 -c user.email=yoBoss283@users.noreply.github.com commit`. Never the owner's real name or
  e-mail. Pull and push from the Terminal panel (the owner's GitHub login is in the macOS keychain).
- **Never put the Sangha statistics repo's other data here** (names, entries, lists): only the yearly totals people.py makes.
- `BRIEF.md` explains the aim for outside reviewers; keep it in step with the page.
