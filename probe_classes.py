import openpyxl
# Data Banat 2026-2027.xlsx
f='.data-pondokbanat/Data Banat 2026-2027.xlsx'
wb = openpyxl.load_workbook(f, read_only=True)
for sn in ['Mata Pelajaran','Data Kelas']:
    ws = wb[sn]
    rows = list(ws.iter_rows(values_only=True))
    data = [r for r in rows if any(c is not None and str(c).strip()!='' for c in r)]
    print('=== %s: %d data rows' % (sn, len(data)))
    if data:
        print('  header:', data[0])
        # unique values in col A and col B
        for ci in range(min(4, len(data[0]))):
            vals = [str(r[ci]).strip() for r in data[1:] if r[ci] is not None and str(r[ci]).strip()]
            uniq = sorted(set(vals))
            print('  col%d unique:', ci, len(uniq))
            print('    ', uniq[:20])
wb.close()
