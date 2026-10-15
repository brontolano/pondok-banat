import os, time, sqlite3, openpyxl

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DATA_DIR = os.path.join(BASE, [e for e in os.listdir(BASE) if e.startswith(".data")][0])

t0 = time.time()
wb = openpyxl.load_workbook(os.path.join(DATA_DIR, "DATA PARA PENGAJAR BANAT.xlsx"), read_only=True)
ws = wb["TAHUN 2026-2027"]
rows = list(ws.iter_rows(values_only=True))
wb.close()
print("rows loaded:", len(rows), "s", round(time.time()-t0, 2), flush=True)

# Simulate the teacher import loop in isolation
t0 = time.time()
conn = sqlite3.connect(os.path.join(BASE, "dev.db"))
conn.row_factory = sqlite3.Row
class_map = {str(r["kode"]): r["id"] for r in conn.execute("SELECT kode, id FROM classes")}
print("class_map:", len(class_map), "s", round(time.time()-t0, 2), flush=True)

inserted = skipped = 0
seen = set()
for r in rows:
    no, nama, kode, jml, jabatan, wali_kelas = r[0], r[1], r[2], r[3], r[4], r[5]
    if no is None or not str(nama).strip():
        continue
    nama = str(nama).strip()
    jabatan = str(jabatan).strip() if jabatan else None
    wali_kelas_id = class_map.get(str(wali_kelas).strip()) if wali_kelas else None
    nip = str(kode).strip() if kode else None
    candidate = nip
    while candidate and candidate in seen:
        candidate = (nip or "NO") + "_" + str(no)
    if candidate:
        seen.add(candidate)
    inserted += 1
print("inserted:", inserted, "s", round(time.time()-t0, 2), flush=True)
conn.close()
