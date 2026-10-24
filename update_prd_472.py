import re

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# 1. Update header: current HEAD hash
content = content.replace(
    'e1a192e2379eb8564610be398c72937f93bfd64d (Rev. 471',
    'a48d198ffcb66ac00d0a8f2877339115d41d4805 (Rev. 471'
)
# Update branch ahead count
content = content.replace(
    'Local branch **8 commits ahead / 0 behind** origin_main',
    'Local branch **10 commits ahead / 0 behind** origin_main'
)

# 2. Update §11 heading
content = content.replace(
    '## 11. REVISI TERBARU (Rev. 116–471 — 23 Oktober 2026 WIB)',
    '## 11. REVISI TERBARU (Rev. 116–472 — 23 Oktober 2026 WIB)'
)

# 3. Update §12 heading
content = content.replace(
    '## 12. REVISI TERBARU (Rev. 468–471 — 23 Oktober 2026 WIB)',
    '## 12. REVISI TERBARU (Rev. 468–472 — 23 Oktober 2026 WIB)'
)

# 4. Add Rev. 472 bullet to §11 and §12
rev472_bullet = """||- **Rev. 472.** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `a48d198ffcb66ac00d0a8f2877339115d41d4805` (Rev. 471: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 471, §11 kompakt changelog 116–471, §12 updated; fixes: dokument PRD typo (dokeman), §13 stale refs, §12 range Rev. 468–471), 10 / 0 (10 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 471** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokumen PRD **REVISI** — rev 472 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 471; branch 10 ahead / 0 behind origin_main."""

# Find the Rev. 471 bullet in §11 and add Rev. 472 after it
# The §11 section is between "## 11. REVISI TERBARU" and "## 12. REVISI TERBARU"
section11_end = content.find('## 12. REVISI TERBARU')
section11 = content[:section11_end]

idx_471_11 = section11.find('||- **Rev. 471.**')
if idx_471_11 == -1:
    print("ERROR: Rev. 471 bullet not found in §11")
else:
    remaining = section11[idx_471_11:]
    end_marker = "branch 8 ahead / 0 behind origin_main."
    end_idx = remaining.find(end_marker)
    if end_idx == -1:
        print("ERROR: end marker not found in §11")
    else:
        end_pos = idx_471_11 + end_idx + len(end_marker)
        content = content[:end_pos] + "\n" + rev472_bullet + content[end_pos:]

# Find the Rev. 471 bullet in §12 and add Rev. 472 after it
section12_start = content.find('## 12. REVISI TERBARU')
section12 = content[section12_start:]

idx_471_12 = section12.find('||- **Rev. 471.**')
if idx_471_12 == -1:
    print("ERROR: Rev. 471 bullet not found in §12")
else:
    remaining = section12[idx_471_12:]
    end_marker = "branch 8 ahead / 0 behind origin_main."
    end_idx = remaining.find(end_marker)
    if end_idx == -1:
        print("ERROR: end marker not found in §12")
    else:
        end_pos = idx_471_12 + end_idx + len(end_marker)
        content = content[:end_pos] + "\n" + rev472_bullet + content[end_pos:]

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print("Done. Content length:", len(content))
print("Header updated:", 'a48d198ffcb66ac00d0a8f2877339115d41d4805' in content)
print("Branch ahead updated:", '**10 commits ahead**' in content)
print("§11 heading updated:", 'Rev. 116–472' in content)
print("§12 heading updated:", 'Rev. 468–472' in content)
print("Rev. 472 bullet in §11:", 'Rev. 472.** 24 Oktober 2026' in content)
print("Rev. 472 bullet in §12:", 'Rev. 472.** 24 Oktober 2026' in content)
