import os, time, sqlite3, openpyxl

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DATA_DIR = os.path.join(BASE, [e for e in os.listdir(BASE) if e.startswith(".data")][0])

t0 = time.time()
wb = openpyxl.load_workbook(os.path.join(DATA_DIR, "DATA PARA PENGAJAR BANAT.xlsx"), read_only=True)
ws = wb["TAHUN 2026-2027"]
rows = list(ws.iter_rows(values_only=True))
wb.close()
print("rows:", len(rows), flush=True)

t0 = time.time()
conn = sqlite3.connect(os.path.join(BASE, "dev.db"))
print("conn open s", round(time.time()-t0, 3), flush=True)
n = 0
for r in conn.execute("SELECT kode, id FROM classes"):
    n += 1
print("classes rows:", n, "s", round(time.time()-t0, 3), flush=True)
conn.close()
print("conn closed s", round(time.time()-t0, 3), flush=True)
