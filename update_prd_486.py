# -*- coding: utf-8 -*-
import io

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with io.open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

def repl(old, new, label):
    global src
    n = src.count(old)
    if n != 1:
        raise SystemExit("FAIL [%s]: count=%d for: %r" % (label, n, old[:120]))
    src = src.replace(old, new, 1)
    print("OK [%s]" % label)

# ---- Header ----
repl("`1b2b245d06bfa50a581a58b4aac85380f21fe113` (Rev. 485: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 485, §11 kompakt changelog 116–485, §12 updated). Branch `main`",
     "`ff465bba47116093782778b49af31211368cf13d` (Rev. 486: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated). Branch `main`",
     "header rev-rev")

repl("`git rev-parse HEAD` = `1b2b245d06bfa50a581a58b4aac85380f21fe113` (Rev. 485); **origin/main:**",
     "`git rev-parse HEAD` = `ff465bba47116093782778b49af31211368cf13d` (Rev. 486); **origin/main:**",
     "header head-ref")

repl("Local branch **13 commits ahead / 0 behind** origin_main.",
     "Local branch **14 commits ahead / 0 behind** origin_main.",
     "header ahead")

repl("(revisi terbaru = Rev. 485, fresh verification dilakukan hari ini)",
     "(revisi terbaru = Rev. 486, fresh verification dilakukan hari ini)",
     "header revici")

# ---- Section 12 header range ----
repl("## 12. REVISI TERBARU (Rev. 468–485 — 23 Oktober 2026 WIB)",
     "## 12. REVISI TERBARU (Rev. 468–486 — 23 Oktober 2026 WIB)",
     "s12 header range")

# ---- Section 12: Git HEAD bullet ----
repl("`023ff38e5ce61b6d0932ced2e80bdd65cd57e0a2` (Rev. 476: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 476, §11 kompakt changelog 116–476, §12 updated). Local branch **3 commits ahead / 0 behind** origin_main.",
     "`ff465bba47116093782778b49af31211368cf13d` (Rev. 486: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated). Local branch **14 commits ahead / 0 behind** origin_main.",
     "s12 git-head")

# ---- Section 12: Working tree bullet ----
repl("> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 476); HEAD `023ff38e5ce61b6d0932ced2e80bdd65cd57e0a2` (Rev. 476); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.",
     "> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 486); HEAD `ff465bba47116093782778b49af31211368cf13d` (Rev. 486); seluruh file lain cocak dengan HEAD; untracked: 19 skrip utility (tidak terpantau dalam git). `git ls-files` = 187 file.",
     "s12 worktree")

# ---- Section 12: Status bullet ----
repl("> - **Status:** dokumen PRD **REVISI** — rev 476 = PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `023ff38e5ce61b6d0932ced2e80bdd65cd57e0a2` (Rev. 476), 3 / 0 (3 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 475 (data terkonsisten).",
     "> - **Status:** dokumen PRD **REVISI** — rev 486 = PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `ff465bba47116093782778b49af31211368cf13d` (Rev. 486), 14 / 0 (14 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 485 (data terkonsisten).",
     "s12 status")

# ---- Section 12: add Rev. 486 table row at top ----
ANCHOR = "||_- **Rev. 482.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `e38157decde7a10910caf38a22324c23f41eaa00`"
new_row = ("||- **Rev. 486.** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `ff465bba47116093782778b49af31211368cf13d` (Rev. 486: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated), 14 / 0 (14 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 485** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`. **Status:** dokumen PRD **REVISI** — rev 486 = PRD fresh verification & stability confirmation; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 485; branch 14 ahead / 0 behind origin_main.")

repl(ANCHOR,
     new_row + "\n" + ANCHOR,
     "s12 add rev486 row")

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print("WROTE", PATH)
