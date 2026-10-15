import os, time, sqlite3, uuid

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DB = os.path.join(BASE, "dev.db")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# Clear teachers
conn.execute("DELETE FROM teachers")
conn.commit()

# Build class map
class_map = {str(r["kode"]): r["id"] for r in conn.execute("SELECT kode, id FROM classes")}
print("class_map:", len(class_map), flush=True)

cur = conn.cursor()
t0 = time.time()

for i in range(60):
    no = i + 1
    nama = f"TEST GURU {i}"
    jabatan = "GURU" if i % 2 == 0 else "WALI KELAS"
    nip = str(i)
    candidate = nip
    while candidate in set():  # no-op placeholder
        pass
    # simulate the same candidate logic
    seen = set()
    candidate = nip
    while candidate and candidate in seen:
        candidate = (nip or "NO") + "_" + str(no)
    if candidate:
        seen.add(candidate)
    cur.execute(
        "INSERT INTO teachers (id, nip, name, jk, jabatan, status, kelas_id, no_hp, email, alamat, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, 'active', ?, ?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), candidate, nama, None, jabatan, None, None, None, None, "2026-10-13T00:00:00", "2026-10-13T00:00:00"),
    )

conn.commit()
print("inserted:", 60, "time:", round(time.time()-t0, 3), "s", flush=True)
conn.close()
