#!/usr/bin/env python3
"""
import_excel.py — Automate import of .data-pondokanat/ Excel data into dev.db.

Targets M03 (Master Data Guru & Staf), per PRD §2.2/M03: reads
`DATA PARA PENGAJAR BANAT.xlsx` > `TAHUN 2026-2027` sheet and imports
teachers into the `teachers` table.  Classes are merged (new kodes only).

Idempotent (teachers cleared and re-imported).

NOTE on data hygiene: the TAHUN 2026-2027 sheet embeds header rows
('NO','NAMA PENGAJAR',...) as plain rows, so rows whose NO/kode are
strings are skipped.  The NIP-uniqueness guard is written so it cannot
loop forever on duplicate NIP values.
"""
import os
import sqlite3
import uuid
from datetime import datetime

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DB = os.path.join(BASE, "dev.db")
DATA_DIR = os.path.join(BASE, [e for e in os.listdir(BASE) if e.startswith(".data")][0])
CURRENT = datetime.now().isoformat(timespec="seconds")


def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def now():
    return CURRENT


def _codes_from_row(r):
    out = []
    for c in r:
        if c is None:
            continue
        s = str(c).strip()
        if s:
            out.append(s)
    return out


def import_classes(conn):
    """Merge: add any new kelas codes found in Data Banat > Data Kelas sheet."""
    import openpyxl

    wb = openpyxl.load_workbook(os.path.join(DATA_DIR, "Data Banat 2026-2027.xlsx"),
                                read_only=True)
    ws = wb["Data Kelas"]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    class_row = None
    for r in rows:
        codes = _codes_from_row(r)
        if codes and codes[0] == "TAKHOSUS":
            class_row = codes
            break

    if not class_row:
        print("  WARNING: no class-code row found in Data Kelas")
        return 0

    cur = conn.cursor()
    existing = set(r[0] for r in cur.execute("SELECT kode FROM classes"))
    inserted = 0
    for code in class_row:
        if code in existing or code == "TAKHOSUS":
            continue
        cur.execute(
            "INSERT INTO classes (id, kode, nama, seksi, jenjang, program, wali_kelas_id, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), code, code,
             None, code if code[0].isdigit() else "Takhosous", None, None, now(), now()),
        )
        inserted += 1
        existing.add(code)
    conn.commit()
    return inserted


def import_teachers(conn):
    """Import guru from DATA PARA PENGAJAR BANAT.xlsx > TAHUN 2026-2027."""
    import openpyxl

    wb = openpyxl.load_workbook(os.path.join(DATA_DIR, "DATA PARA PENGAJAR BANAT.xlsx"),
                                read_only=True)
    ws = wb["TAHUN 2026-2027"]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    class_map = {str(r[0]): r[1] for r in conn.execute("SELECT kode, id FROM classes")}

    cur = conn.cursor()
    cur.execute("DELETE FROM teachers")
    conn.commit()

    inserted = skipped = 0
    seen_nip = set()
    for r in rows:
        no, nama, kode, jml, jabatan, wali_kelas = r[0], r[1], r[2], r[3], r[4], r[5]

        # Skip header rows (their NO/KODE/jabatan are string literals like 'NO'/'KODE')
        # NOTE: jabatan is a free-text field (e.g. "MUDIR'AM") and must NOT be type-checked.
        if isinstance(no, str):
            continue
        if no is None or not str(nama).strip():
            continue

        nama = str(nama).strip()
        jabatan = str(jabatan).strip() if jabatan else None
        wali_kelas_id = class_map.get(str(wali_kelas).strip()) if wali_kelas else None
        nip = str(kode).strip() if kode else None

        # build a unique NIP: append a suffix only when the base is taken
        candidate = nip
        while candidate and candidate in seen_nip:
            candidate = candidate + "_" + str(no)
        if candidate:
            seen_nip.add(candidate)

        try:
            cur.execute(
                "INSERT INTO teachers (id, nip, name, jk, jabatan, status, kelas_id, no_hp, email, alamat, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, 'active', ?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4()), candidate, nama, None, jabatan, wali_kelas_id, None, None, None, now(), now()),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            skipped += 1
    conn.commit()
    return inserted, skipped


def main():
    conn = connect()
    try:
        n_cls = import_classes(conn)
        n_teach, n_skip = import_teachers(conn)
        print("classes merged (new):", n_cls)
        print("teachers imported:", n_teach, "skipped:", n_skip)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
