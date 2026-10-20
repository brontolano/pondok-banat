path = "PRD-PONDOK-BANAT.md"
content = open(path).read()

changes = []


def rep(old, new, count=1):
    global content
    if old in content:
        content = content.replace(old, new, count)
        changes.append(old[:60] + "..." if len(old) > 60 else old)
        return True
    else:
        print("NOT FOUND: " + old[:80])
        return False


# --- 1. Header (line 4) ---
rep("**Rev. 362", "**Rev. 363")
rep("`a5f0c77`", "`b6e9e0c`")
rep("(Rev. 361, commit `a5f0c7774f06a995460549fcfcc7a72b4b718800`)", "(Rev. 362, commit `b6e9e0cb8ef8109d5da51936eb60535f2f96cdfd`)")
rep("`a5f0c7774f06a995460549fcfcc7a72b4b718800`", "`b6e9e0cb8ef8109d5da51936eb60535f2f96cdfd`")
rep("Local branch **8 commits ahead**", "Local branch **9 commits ahead**")
rep("revisi terbaru = Rev. 362", "revisi terbaru = Rev. 363")

# --- 2. Section 146 -> 147 title ---
rep("## 146. REVISI TERBARU (Rev. 362", "## 147. REVISI TERBARU (Rev. 363")

# --- 3. Section 146 bullet ---
rep(
    "   - **Git HEAD (local):** `a5f0c77` (Rev. 361, commit `a5f0c7774f06a995460549fcfcc7a72b4b718800`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `a5f0c7774f06a995460549fcfcc7a72b4b718800`). **origin/main:** `8df4a80` (Rev. 353). Local branch **8 commits ahead**, **0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 362); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 113 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py).",
    "   - **Git HEAD (local):** `b6e9e0c` (Rev. 362, commit `b6e9e0cb8ef8109d5da51936eb60535f2f96cdfd`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b6e9e0cb8ef8109d5da51936eb60535f2f96cdfd`). **origin/main:** `8df4a80` (Rev. 353). Local branch **9 commits ahead**, **0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 363); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 113 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py).",
)

# --- 4. Section 146 status ---
rep(
    "3. **Status:** dokumen PRD **REVISI** \u2014 rev 362 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 362**. Git HEAD = `a5f0c77` (Rev. 361, 8 commits ahead origin.main.).",
    "3. **Status:** dokumen PRD **REVISI** \u2014 rev 363 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 363**. Git HEAD = `b6e9e0c` (Rev. 362, 9 commits ahead origin.main.).",
)

# --- 5. Section 146 changes-from ---
rep(
    "2. **Perubahan dari Rev. 361:**\n   - **Header PRD:** diperbarui ke **Rev. 362** (tanggal 20 Oktober 2026 WIB).\n   - **New Section 146 (Rev. 362):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 362.\n   - **Referensi HEAD:** state terkini HEAD = `a5f0c77` (Rev. 361, commit `a5f0c7774f06a995460549fcfcc7a72b4b718800`); origin/main = `8df4a80` (Rev. 353). Branch **8 commits ahead** origin.main.",
    "2. **Perubahan dari Rev. 362:**\n   - **Header PRD:** diperbarui ke **Rev. 363** (tanggal 20 Oktober 2026 WIB).\n   - **New Section 147 (Rev. 363):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 363.\n   - **Referensi HEAD:** state terkini HEAD = `b6e9e0c` (Rev. 362, commit `b6e9e0cb8ef8109d5da51936eb60535f2f96cdfd`); origin/main = `8df4a80` (Rev. 353). Branch **9 commits ahead** origin.main.",
)

# --- 6. Section 148 append ---
# The marker is the NEW section 146 status (after replacement)
marker = "3. **Status:** dokumen PRD **REVISI** \u2014 rev 363 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 363**. Git HEAD = `b6e9e0c` (Rev. 362, 9 commits ahead origin.main.)."

new_section = """
3. **Status:** dokumen PRD **REVISI** \u2014 rev 363 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 363**. Git HEAD = `b6e9e0c` (Rev. 362, 9 commits ahead origin.main.).

## 148. REVISI TERBARU (Rev. 363 \u2014 20 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 20 Oktober 2026 (WIB, cron run) \u2014 pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / struktur source / skema Prisma / Login.tsx / Beranda.tsx. Semua data diverifikasi langsung dari repo kerja saat ini.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 362 (data terkonsisten).**  
   - **Git HEAD (local):** `b6e9e0c` (Rev. 362, commit `b6e9e0cb8ef8109d5da51936eb60535f2f96cdfd`). Branch `main` (remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b6e9e0cb8ef8109d5da51936eb60535f2f96cdfd`). **origin/main:** `8df4a80` (Rev. 353). Local branch **9 commits ahead**, **0 commit behind** origin.main. Working tree: PRD cocak dengan HEAD (revisi terbaru = Rev. 363); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file; 113 file tidak ter-track (skrip sementara, backup, section .md, .orig, .py).  
   - **Database (dev.db):** file `dev.db` saat ini **absent** \u2014 dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).  
   - **Build quality gate:** **NO LONGER RE-RUNABLE** \u2014 `node_modules/` absen (0 package; `.bin` tidak ada). `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). `tsc --noEmit` -> exit 1; `eslint .` -> exit 2; `next build` -> exit 1 (semua gagal karena dependency tidak tersedia, memerlukan `npm install` ulang).  
   - **Prisma schema:** 17 model terdefinisi (termasuk `KitabProgress` di baris 203, `Sertakan` di baris 218 \u2014 ditambahkan Rev. 51). `uidNfc` pada model `Student` (baris 68, `uidNfc String? @map(\\"uid_nfc\\")`). `prisma/schema.prisma` **263 baris**, 8492 bytes. `prisma validate` **tidak dapat dijalankan** karena `prisma` CLI tidak terinstall (`node_modules` absen).  
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\\"uid_nfc\\"` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) \u2014 data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).  
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` \u2014 sesuai nama Pondok Banat). Produksi butuh bcrypt + session.  
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26--28) & `src/app/beranda/page.tsx` (baris 14--16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB; sudah diperbarui ke 453 sesuai data Excel grade sheets).  
   - **Source files:** `src/app/*` = 15 entri (12 sub direktori: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + globals.css, layout.tsx, page.tsx); `src/components` = 2 (Beranda.tsx & Login.tsx); `src/lib` = kosong (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).  
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.

2. **Perubahan dari Rev. 362:**  
   - **Header PRD:** diperbarui ke **Rev. 363** (tanggal 20 Oktober 2026 WIB).  
   - **Referensi HEAD:** state terkini HEAD = `b6e9e0c` (Rev. 362, commit `b6e9e0cb8ef8109d5da51936eb60535f2f96cdfd`); origin/main = `8df4a80` (Rev. 353). Branch **9 commits ahead** origin.main.  
   - **Bundled scripts:** `update_prd_362.py` (--20 Oktober 2026) dihasilkan dari *fresh verification* Rev. 362; konsolidasi nanti ke `update_prd_363.py` bila diperlukan.  
   - **Status:** dokumen PRD **REVISI** \u2014 rev 363 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 363**. Git HEAD = `b6e9e0c` (Rev. 362, 9 commits ahead origin.main.).

"""

if marker in content:
    content = content.replace(marker, new_section, 1)
    changes.append("section 148 added")
    print("Section 148 (Rev. 363) added.")
else:
    print("ERROR: section 147 marker NOT found in content")
    print("Last 1200 chars of content:")
    print(repr(content[-1200:]))


# Verify
if "**Rev. 363" in content and "9 commits ahead" in content and "## 148. REVISI TERBARU (Rev. 363" in content:
    open(path, "w").write(content)
    print("\nSUCCESS. Changes applied: " + str(len(changes)))
    for c in changes:
        print(" - " + c)
else:
    print("\nERROR: verification checks failed")
    print("  '**Rev. 363' in content:", "**Rev. 363" in content)
    print("  '9 commits ahead' in content:", "9 commits ahead" in content)
    print("  '## 148. REVISI TERBARU' in content:", "## 148. REVISI TERBARU" in content)
