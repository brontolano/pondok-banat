import openpyxl
from collections import Counter, OrderedDict
import os

base = '.data-pondokbanat'

# Teacher count
f = os.path.join(base, 'DATA PARA PENGAJAR BANAT.xlsx')
wb = openpyxl.load_workbook(f, read_only=True)
ws = wb['Table 1']
rows = list(ws.iter_rows(values_only=True))
main_teacher_rows = rows[2:89]
badal_rows = rows[92:99]
def names_from(rows_slice):
    names = []
    nos = []
    for r in rows_slice:
        no = r[0]
        nama = r[1]
        if no is not None and nama:
            nos.append(no)
            names.append(str(nama).strip())
    return names, nos
mn, mnos = names_from(main_teacher_rows)
bn, bnos = names_from(badal_rows)
print('MAIN TEACHERS:', len(mn), 'unique NO:', len(OrderedDict.fromkeys(mnos)))
print('BADAL TEACHERS:', len(bn), 'unique NO:', len(OrderedDict.fromkeys(bnos)))
print('Total data rows:', len(mn)+len(bn))
print('Duplicate names (main):', [n for n,c in Counter(mn).items() if c>1])
print('First 5 main:', mn[:5])
print('Badal:', bn)
wb.close()
