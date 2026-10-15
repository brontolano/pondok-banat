import openpyxl, os
from collections import OrderedDict

base = "/opt/data/home/workspace/dev/pondok-banat/.data-pondokbanat"

# Investigate Table 1 full structure
f = os.path.join(base, "DATA PARA PENGAJAR BANAT.xlsx")
wb = openpyxl.load_workbook(f, read_only=True)
ws = wb["Table 1"]
rows = list(ws.iter_rows(values_only=True))
print("Table 1 total rows:", len(rows))
print("--- First 15 rows (all cols) ---")
for i, r in enumerate(rows[:15]):
    print(i, ":", r)
print("--- Last 10 rows ---")
for i, r in enumerate(rows[-10:]):
    print(len(rows)-10+i, ":", r)
wb.close()
