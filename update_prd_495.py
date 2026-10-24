import os
p = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

def rep(old, new):
    global content
    if old not in content:
        raise AssertionError("NOT FOUND: " + old[:80])
    content = content.replace(old, new, 1)
    print("OK:", old[:60])

# ===== HEADER (line 4) =====
rep('Rev. 494 (final): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 494',
    'Rev. 495 (final): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 495')
rep('§11 kompakt changelog 116–492', '§11 kompakt changelog 116–495')
rep('HEAD `c01c1e6` (Rev. 494)', 'HEAD `b1aec91fbc7b97e87f71908b6019f5d335ce8975` (Rev. 495)')
rep('Local branch **24 commits ahead / 0 behind**', 'Local branch **26 commits ahead / 0 behind**')
rep('`git rev-parse HEAD` = `c01c1e6e45cc5388ab09cd15861d9b2e27b801db` (Rev. 494 (final)',
    '`git rev-parse HEAD` = `b1aec91fbc7b97e87f71908b6019f5d335ce8975` (Rev. 495 (final)')

# ===== §11 header (line 413) =====
rep('## 11. REVISI TERBARU (Rev. 116–492 — 23 Oktober 2026 WIB)',
    '## 11. REVISI TERBARU (Rev. 116–495 — 23 Oktober 2026 WIB)')

# ===== §11 list: add Rev. 495 entry after Rev. 491 entry (line 422) =====
old491 = '''    491. 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `94d19e3175718470e7214641aee6e0cb46f34177` (Rev. 490 commit), 20 / 0 (20 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 490** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 491 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 490; branch 20 ahead / 0 behind origin_main.'''
new495 = old491 + '''
    495. 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `b1aec91fbc7b97e87f71908b6019f5d335ce8975` (Rev. 495 commit), 26 / 0 (26 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 494** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 495 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 494; branch 26 ahead / 0 behind origin_main.'''
rep(old491, new495)

# ===== §12 header (line 423) =====
rep('## 12. REVISI TERBARU (Rev. 468–493 — 23 Oktober 2026 WIB)',
    '## 12. REVISI TERBARU (Rev. 468–495 — 23 Oktober 2026 WIB)')

# ===== §12 blockquote (lines 425-437) =====
rep('9d7fe316159efa9c781fa0263187a7e707', 'b1aec91fbc7b97e87f71908b6019f5d335ce8975')
rep('Rev. 486 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 486, §11 kompakt changelog 116–485, §12 updated',
    'Rev. 495 (final): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 495, §11 kompakt changelog 116–495, §12 updated')
rep('**16 commits ahead / 0 behind**', '**26 commits ahead / 0 behind**')

# ===== §12 table: add Rev. 495 entry after Rev. 494 entry (line 483) =====
old494_table = '||- **Rev. 494 (final).** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `c01c1e6` (Rev. 493 final commit), 24 / 0 (24 commits ahead origin_main).'
new495_table = old494_table + '''
||- **Rev. 495 (final).** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `b1aec91fbc7b97e87f71908b6019f5d335ce8975` (Rev. 495 (final): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 495, §11 kompakt changelog 116–495, §12 updated), 26 / 0 (26 commits ahead origin_main).'''
rep(old494_table, new495_table)

with open(p, 'w', encoding='utf-8') as f:
    f.write(content)

print("DONE. New file length:", len(content))
print("Rev. 495 in file:", 'Rev. 495' in content)
print("b1aec91 in file:", 'b1aec91fbc7b97e87f71908b6019f5d335ce8975' in content)
print("9d7fe31 in file:", content.count('9d7fe316159efa9c781fa0263187a7e707'))
print("26 / 0 in file:", '26 / 0' in content or '26 commits ahead' in content)
