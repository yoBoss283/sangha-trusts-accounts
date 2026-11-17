# Turn each annual report PDF in accounts/ into plain text in txt/<year>.txt, keeping the column layout.
# The year is the year the accounts end in (31 March). Run: venv/bin/python extract.py
#
# Reports with a text layer are read with pypdf. Reports that are only images (the Companies House scans)
# are read with ./ocr (the Mac's own text recognition, see ocr.swift) and laid out again into rows and columns.
# Text already made is kept; delete txt/<year>.txt to read a report again.
# When two files cover the same year, the one from the Trust (not "Companies_House_") is used.
import pathlib, re, sys, logging, subprocess
import pypdf

logging.getLogger('pypdf').setLevel(logging.ERROR)   # font warnings from scanned reports are harmless
here = pathlib.Path(__file__).parent
(here / 'txt').mkdir(exist_ok=True)
WIDTH = 170                                          # characters across a page in the laid-out text


def layout(tsv):
    """Rows of recognised text -> lines: pieces at the same height become one line, placed by their x position."""
    pages = {}
    for line in tsv.splitlines():
        p, x, y, w, h, t = line.split('\t', 5)
        pages.setdefault(int(p), []).append((float(y) + float(h) / 2, float(x), float(h), t))
    out = []
    for p in sorted(pages):
        out.append(f'=== page {p} ===')
        rows = []
        for yc, x, h, t in sorted(pages[p]):
            if rows and abs(yc - rows[-1][0]) < max(0.004, 0.45 * h):
                rows[-1][1].append((x, t))
            else:
                rows.append([yc, [(x, t)]])
        for _, pieces in rows:
            s = ''
            for x, t in sorted(pieces):
                col = int(round(x * WIDTH))
                s += ' ' * max(2 if s else 0, col - len(s)) + t
            out.append(s)
    return '\n'.join(out) + '\n'


def year_of(pdf):
    m = re.search(r'(20\d\d|19\d\d)', pdf.stem)
    if not m:
        sys.exit(f'{pdf.name}: no year in the file name')
    return m.group(1)


pdfs = sorted((here / 'accounts').glob('*.pdf'), key=lambda p: ('Companies_House_' in p.name, p.name))
done = set()
for pdf in pdfs:
    y = year_of(pdf)
    if y in done:
        continue                                     # the Trust's own copy came first
    done.add(y)
    out = here / 'txt' / f'{y}.txt'
    if out.exists() and out.stat().st_mtime > pdf.stat().st_mtime:
        continue
    r = pypdf.PdfReader(pdf)
    pages = [p.extract_text(extraction_mode='layout') or '' for p in r.pages]
    if sum(len(p.strip()) for p in pages) > 2000:
        text, how = '\n'.join(f'=== page {i + 1} ===\n' + p for i, p in enumerate(pages)), 'text'
    else:
        if not (here / 'ocr').exists():
            subprocess.run(['swiftc', '-O', str(here / 'ocr.swift'), '-o', str(here / 'ocr')], check=True)
        tsv = subprocess.run([str(here / 'ocr'), str(pdf)], check=True, capture_output=True, text=True).stdout
        text, how = layout(tsv), 'scan, read by text recognition'
    out.write_text(text, encoding='utf-8')
    print(f'{y}: {pdf.name}, {len(r.pages)} pages ({how})', flush=True)
