# What it costs to run the monasteries

A landing page and three plain-language reports on what it costs to run four UK monasteries, written from the three
charitable trusts' own published annual accounts (Companies House and the Charity Commission register).

- `index.html`: the landing page, one card for each trust.
- `pages/est.html`: Amaravati and Chithurst (English Sangha Trust).
- `pages/ratanagiri.html`: Aruna Ratanagiri (Harnham Buddhist Monastery Trust).
- `pages/hartridge.html`: Hartridge (Hartridge Buddhist Monastery Trust).

Each page works on its own (open it in any browser, also offline). Only yearly totals are used: the amounts from the
accounts and the yearly count of residents from the community lists. No names.

The English Sangha Trust report is built from https://github.com/yoBoss283/sangha-accounts-statistics. `build.py` here
rebuilds the landing page and copies the three finished reports into `pages/`; it expects the three source folders next
to this one, so it is for whoever keeps the reports, not needed to read them.
