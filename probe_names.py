import openpyxl
f='.data-pondokbanat/DATA PARA PENGAJAR BANAT.xlsx'
wb = openpyxl.load_workbook(f, read_only=True)
ws = wb['Table 1']
rows = list(ws.iter_rows(values_only=True))
data = [r for r in rows if any(c is not None and str(c).strip()!='' for c in r)]
print('Table 1 total data rows:', len(data))
if data:
    hdr = data[0]
    print('Header:', hdr)
    for i,h in enumerate(hdr):
        hs=str(h).lower()
        if any(k in hs for k in ['nama','name','guru','staf']):
            names = [str(r[i]).strip() for r in data[1:] if r[i] is not None and str(r[i]).strip()]
            print('Column index', i, 'header', h, 'unique names:', len(set(names)))
            print('  sample:', sorted(set(names))[:12])
            break
wb.close()
