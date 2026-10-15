import os, time, sqlite3, openpyxl

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DATA_DIR = os.path.join(BASE, [e for e in os.listdir(BASE) if e.startswith(".data")][0])

# Test import_classes
t0 = time.time()
wb = openpyxl.load_workbook(os.path.join(DATA_DIR, "Data Banat 2026-2027.xlsx"), read_only=True)
ws = wb["Data Kelas"]
rows = list(ws.iter_rows(values_only=True))
wb.close()
print("Data Kelas loaded:", len(rows), "s", round(time.time()-t0, 3), flush=True)

class_row = None
for r in rows:
    codes = [str(c).strip() for c in r if c is not None and str(c).strip()]
    if codes and codes[0] == "TAKHOSUS":
        class_row = codes
        break
print("class_row found:", class_row is not None, flush=True)
print("class_row:", class_row, flush=True)
