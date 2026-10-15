import os
import sqlite3
import time
import openpyxl
import uuid
from datetime import datetime

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DB = os.path.join(BASE, "dev.db")
DATA_DIR = os.path.join(BASE, [e for e in os.listdir(BASE) if e.startswith(".data")][0])

print("DATA_DIR =", DATA_DIR, flush=True)

# ---- Step 1: read teacher sheet ----
t0 = time.perf_counter()
import openpyxl as _op
wb = _op.load_workbook(os.path.join(DATA_DIR, "DATA PARA PENGAJAR BANAT.xlsx"), read_only=True)
ws = wb["TAHUN 2026-2027"]
rows = list(ws.iter_rows(values_only=True))
wb.close()
print("read teachers sheet:", len(rows), "rows,", round(time.perf_counter()-t0, 3), "s", flush=True)

# ---- Step 2: open DB, build class map ----
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
t0 = time.perf_counter()
class_map = {str(r["kode"]): r["id"] for r in conn.execute("SELECT kode, id FROM classes")}
print("class_map built:", len(class_map), "s", round(time.perf_counter()-t0, 3), flush=True)

# ---- Step 3: clear + insert ----
cur = conn.cursor()
t0 = time.perf_counter()
cur.execute("DELETE FROM teachers")
conn.commit()
print("cleared teachers, s", round(time.perf_counter()-t0, 3), flush=True)

seen = set()
inserted = skipped = 0
t0 = time.perf_counter()
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
    try:
        cur.execute(
            "INSERT INTO teachers (id, nip, name, jk, jabatan, status, kelas_id, no_hp, email, alamat, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, 'active', ?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), candidate, nama, None, jabatan, wali_kelas_id, None, None, None,
             "2026-10-13T00:00:00", "2026-10-13T00:00:00"),
        )
        inserted += 1
    except sqlite3.IntegrityError:
        skipped += 1
conn.commit()
print("inserted:", inserted, "skipped:", skipped, "s", round(time.perf_counter()-t0, 3), flush=True)
conn.close()
