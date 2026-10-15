path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, encoding="utf-8") as f:
    lines = f.read().split("\n")

# 1) Rewrite the bloated header (line index 3) as a clean, concise Rev. 76 summary.
clean_header = (
    "> **Rev. 76 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): "
    "state stabil. **Tidak ada perubahan signifikan dari Rev. 75** (data terkonsisten). "
    "**Database (dev.db):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | "
    "**33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | "
    "**18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | "
    "**54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | "
    "**0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. "
    "**Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, "
    "4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. "
    "**M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); "
    "`prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. "
    "**Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). "
    "**Schema:** model `KitabProgress` (Student + Subject) & `Sertakan` (User) selesai didefinisikan (Rev. 51); `prisma validate` sukses. "
    "**Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); "
    "**catatan: DB memiliki `admin@pondokanat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session. "
    "**Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). "
    "**Build quality gate (Verifikasi Rev. 76):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — 0 error); "
    "`npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3)."
)
assert "> **Rev. 75" in lines[3]
lines[3] = clean_header

# 2) Renumber Rev.75 item: substring "4. **Rev. 75" -> "5. **Rev. 75" (only line 533 has it).
n75 = sum(1 for l in lines if "4. **Rev. 75" in l)
assert n75 == 1, "rev75 occurrences: %d" % n75
lines = [l.replace("4. **Rev. 75", "5. **Rev. 75") if "4. **Rev. 75" in l else l for l in lines]

# 3) Insert Rev.76 item after the Rev.75 item line (which ends with "dari Rev. 74.").
idx = None
for i, l in enumerate(lines):
    if l.startswith("5. **Rev. 75 — 15 Oktober 2026") and "dari Rev. 74." in l:
        idx = i
        break
assert idx is not None, "rev75 item not found"
rev76_item = (
    "\n6. **Rev. 76 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. "
    "**Tidak ada perubahan signifikan dari Rev. 75** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: "
    "**Database**: 1 user (admin@pondokanat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (semua `inactive`, `uid_nfc` = 0 terisi) | "
    "18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. "
    "Siswa per kelas (diverifikasi dari `dev.db`): TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, "
    "5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. "
    "**M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). "
    "**Auth hardcode** masih ada. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). "
    "**Build quality gate:** `tsc --noEmit` ✓ exit 0; `npm run lint` ✓ exit 0 (1 warning, 0 error); `npm run build` ✓ exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). "
    "**Status:** dokumen PRD **REVISI** — rev 76 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 75."
)
lines.insert(idx + 1, rev76_item)

with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("wrote", len(lines), "lines; inserted Rev.76 at index", idx + 1)
