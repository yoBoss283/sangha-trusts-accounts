# Reads the two pages of report.pdf ("Report to Abbots 2012-2026", Sumedharama, in euros) into raw_expenses.json (page 1) and
# raw_balance.json (page 2). The table has blank cells, so plain text extraction loses the columns; every number is placed in
# its year by its position on the page. Then: python3 make_data.py (merges rows with the same label, checks totals, writes data.json).
import pypdf, re, json, collections, pathlib
here = pathlib.Path(__file__).parent
pdf = pypdf.PdfReader(here / 'report.pdf')
def items(page):
    out = []
    pdf.pages[page].extract_text(visitor_text=lambda t, cm, tm, fd, fs: out.append((tm[5], tm[4], t.strip())) if t.strip() else None)
    return out
def rows_of(its, cent, label_x, num_x, isnum, width):
    labels = [(y, t) for y, x, t in its if x < label_x and not isnum(t)]
    rows = collections.defaultdict(dict)
    for y, x, t in its:
        if x >= num_x and isnum(t):
            cx = x + len(t.replace('€', '').strip()) * width
            yr = min(cent, key=lambda k: abs(cent[k] - cx))
            if abs(cent[yr] - cx) > 14: continue
            rows[round(y)][yr] = float(t.replace('€', '').replace(',', '').strip())
    lab = lambda y: ' '.join(t for ly, t in labels if abs(ly - y) < 3.5)
    return [(lab(y), rows[y]) for y in sorted(rows, reverse=True)]
p1 = items(0)
hdr = {t: x for y, x, t in p1 if re.fullmatch(r'20\d\d', t)}
json.dump(rows_of(p1, {y: x + 10 for y, x in hdr.items()}, 255, 255, lambda t: re.fullmatch(r'-?[\d,]+(\.\d\d)?', t), 1.55), open(here / 'raw_expenses.json', 'w'), indent=1)
H = [('2025', 242), ('2024', 272), ('2023', 320), ('2022', 358), ('2021', 396), ('2020', 434), ('2019', 472), ('2018', 510), ('2017', 545), ('2016', 584), ('2015', 623), ('2014', 661), ('2013', 696), ('2012', 732), ('2011', 768)]
json.dump(rows_of(items(1), {y: x + 16 for y, x in H}, 190, 220, lambda t: re.fullmatch(r'-?[\d,]+\.\d\d(\s*€)?', t), 1.6), open(here / 'raw_balance.json', 'w'))
print('raw_expenses.json, raw_balance.json written')
