#!/usr/bin/env python3
"""Keep a copy of the site as it is now, before an update:  python3 archive.py [label]

Copies index.html and pages/*.html into archive/<label>/ (default label: this month, e.g. 2026-11), adds a short
"archived copy" line at the top of each page with a link to the latest version, and leaves the live pages alone.
Run it BEFORE adding new reports (UPDATE.md, step 0), then rebuild with `sh build_all.sh`: the landing page lists
every copy in archive/ under "Earlier versions". It refuses to overwrite a copy that already exists.
"""
import datetime, pathlib, re, shutil, sys
here = pathlib.Path(__file__).parent
label = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().strftime('%Y-%m')
if not re.fullmatch(r'\d{4}-\d{2}(-[A-Za-z0-9]+)?', label): sys.exit('label looks like 2026-11')
dest = here / 'archive' / label
if dest.exists(): sys.exit(f'archive/{label} already exists: not overwritten (pick another label, e.g. {label}-b)')
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
when = f'{months[int(label[5:7]) - 1]} {label[:4]}'
(dest / 'pages').mkdir(parents=True)
def banner(depth):
    up = '../' * depth
    return (f'\n<p class="archived" style="font-size:13px;margin:0 0 14px;padding:8px 12px;border:1px solid var(--axis);border-radius:8px;background:var(--surface)">Archived copy: the site as published in {when}. '
            f'<a href="{up}index.html">See the latest version</a></p>')
def copy(src, out, depth):
    h = src.read_text(encoding='utf-8')
    h = re.sub(r'<!--earlier-->.*?<!--/earlier-->', '', h, flags=re.S)       # the list of copies is only on the live page
    h, n = re.subn(r'(<main[^>]*>)', lambda m: m.group(1) + banner(depth), h, count=1)
    assert n == 1, src
    out.write_text(h, encoding='utf-8')
copy(here / 'index.html', dest / 'index.html', 2)
for f in sorted((here / 'pages').glob('*.html')): copy(f, dest / 'pages' / f.name, 3)
print(f'archive/{label}: {1 + len(list((dest / "pages").glob("*.html")))} pages saved ({when})')
