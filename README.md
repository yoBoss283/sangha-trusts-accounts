# What it costs to run the monasteries

One repository, one public page: https://yoboss283.github.io/sangha-trusts-accounts/ . Plain-language reports on what it costs to
run five monasteries, from their own published accounts (Companies House and the Charity Commission register) and, for
Sumedharama in Portugal, the community's own report (in euros). Only yearly totals are used; the yearly count of residents comes
from the community lists. No names.

| Folder | Monastery | Source | Report |
|---|---|---|---|
| `est/` | Amaravati and Chithurst (English Sangha Trust) | annual accounts 1995–2026 | `/est/` |
| `aruna-ratanagiri/` | Aruna Ratanagiri (Harnham Buddhist Monastery Trust) | annual accounts | `/aruna-ratanagiri/` |
| `hartridge/` | Hartridge (Hartridge Buddhist Monastery Trust) | annual accounts | `/hartridge/` |
| `sumedharama/` | Sumedharama, Portugal | the community's report to the abbots, in euros | `/sumedharama/` |

- `index.html`: the landing page, one card for each place. `pages/*.html`: the same reports at the addresses first shared.
- Each folder has its own `README.md`: the source documents, the scripts that read them, `data.json` (every figure by year),
  `template.html` and the built page. `sh build.sh` in a folder rebuilds it from the documents.
- `sh build_all.sh` rebuilds every report page from its saved data, then the landing page.

This is the only repo and the only site. The four earlier separate repos and the old Claude page were retired on 17 Nov 2026.
