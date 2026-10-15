path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Header update: Rev. 46 -> Rev. 47
content = content.replace(
    '> **Rev. 46 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 45** (data terkonsisten).',
    '> **Rev. 47 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 46** (data terkonsisten).'
)

# Header build quality gate label
content = content.replace(
    '**Build quality gate (Verifikasi Rev. 46):**',
    '**Build quality gate (Verifikasi Rev. 47):**'
)

# Entry 24 (Rev. 47) to append at end of section 10.2
entry = '''
24. **Rev. 47 — 15 Oktober 2026 (WIB).** Fresh verification seluruh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 46**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via `.seed_users_roles.py`) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress:** masih *referenced* di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di `prisma/schema.prisma` (baris 117) — perlu ditambahkan kalau fitur progress kitab dibangun. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 47 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 46).
'''

# Append after the Rev. 46 entry. The Rev. 46 entry ends with: ...tidak ada perubahan dari Rev. 45).
marker = 'dari Rev. 45).'
assert marker in content, "marker not found"
content = content.replace(marker, marker + entry, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. New length:", len(content))
