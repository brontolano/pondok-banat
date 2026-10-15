import os, time, sqlite3, openpyxl

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DATA_DIR = os.path.join(BASE, [e for e in os.listdir(BASE) if e.startswith(".data")][0])
print("DATA_DIR:", DATA_DIR)

# Time openpyxl load TAHUN sheet
t0 = time.time()
wb = openpyxl.load_workbook(os.path.join(DATA_DIR, "DATA PARA PENGAJAR BANAT.xlsx"), read_only=True)
ws = wb["TAHUN 2026-2027"]
rows = list(ws.iter_rows(values_only=True))
print("TAHUN load time:", round(time.time()-t0, 2), "s, rows:", len(rows))
wb.close()

# Time openpyxl load Data Kelas
t0 = time.time()
wb = openpyxl.load_workbook(os.path.join(DATA_DIR, "Data Banat 2026-2027.xlsx"), read_only=True)
ws = wb["Data Kelas"]
rows2 = list(ws.iter_rows(values_only=True))
print("Data Kelas load time:", round(time.time()-t0, 2), "s, rows:", len(rows2))
wb.close()
