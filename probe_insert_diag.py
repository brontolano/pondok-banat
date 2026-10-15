import os, time, sqlite3, openpyxl, uuid

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DATA_DIR = os.path.join(BASE, [e for e in os.listdir(BASE) if e.startswith(".data")][0])

wb = openpyxl.load_workbook(os.path.join(DATA_DIR, "DATA PARA PENGAJAR BANAT.xlsx"), read_only=True)
ws = wb["TAHUN 2026-2027"]
rows = list(ws.iter_rows(values_only=True))
wb.close()
print("n rows:", len(rows), flush=True)

# Step A: just iterate and time each row (no insert)
t0 = time.perf_counter()
for i, r in enumerate(rows):
    no, nama, kode, jml, jabatan, wali_kelas = r[0], r[1], r[2], r[3], r[4], r[5]
    if no is None:
        continue
    nama = str(nama).strip()
    jabatan = str(jabatan).strip() if jabatan else None
    wali_kelas_id = None
    nip = str(kode).strip() if kode else None
    candidate = nip
    while candidate and candidate in set():
        candidate = (nip or "NO") + "_" + str(no)
    if i % 10 == 0:
        print(f"  row {i}: no={no!r} nama={nama!r} kode={kode!r} jabatan={jabatan!r} wali={wali_kelas!r} nip={nip!r}", flush=True)
print("iterate only, s:", round(time.perf_counter()-t0, 3), flush=True)

# Step B: now do the insert but time each row
t0 = time.perf_counter()
conn = sqlite3.connect(os.path.join(BASE, "dev.db"))
conn.row_factory = sqlite3.Row
class_map = {str(r["kode"]): r["id"] for r in conn.execute("SELECT kode, id FROM classes")}
cur = conn.cursor()
inserted = 0
for i, r in enumerate(rows):
    no, nama, kode, jml, jabatan, wali_kelas = r[0], r[1], r[2], r[3], r[4], r[5]
    if no is None or not str(nama).strip():
        continue
    nama = str(nama).strip()
    jabatan = str(jabatan).strip() if jabatan else None
    wali_kelas_id = class_map.get(str(wali_kelas).strip()) if wali_kelas else None
    nip = str(kode).strip() if kode else None
    candidate = nip
    while candidate and candidate in set():
        candidate = (nip or "NO") + "_" + str(no)
    if candidate and candidate not in set():
        pass
    try:
        cur.execute(
            "INSERT INTO teachers (id, nip, name, jk, jabatan, status, kelas_id, no_hp, email, alamat, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, 'active', ?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), candidate, nama, None, jabatan, wali_kelas_id, None, None, None,
             "2026-10-13T00:00:00", "2026-10-13T00:00:00"),
        )
        inserted += 1
    except sqlite3.IntegrityError:
        pass
conn.commit()
print("inserted:", inserted, "s:", round(time.perf_counter()-t0, 3), flush=True)
conn.close()
