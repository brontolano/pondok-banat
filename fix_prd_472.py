#!/usr/bin/env python3
"""Fix PRD-PONDOK-BANAT.md: correct Rev. 472 bullet placement + header hash."""

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r') as f:
    content = f.read()

# --- Step 1: Update header git HEAD hash ---
old_hash = 'e1a192e2379eb8564610be398c72937f93bfd64d (Rev. 471'
new_hash = 'a48d198ffcb66ac00d0a8f2877339115d41d4805 (Rev. 471'
count_hash = content.count(old_hash)
print(f"Hash occurrences: {count_hash}")
content = content.replace(old_hash, new_hash)

# --- Step 2: Remove the misplaced Rev. 472 bullet (currently at line 224) ---
# The bullet to remove starts with: ||- **Rev. 472.** 24 Oktober 2026 (WIB): ...
# and ends with: branch 10 ahead / 0 behind origin_main.
rev472_bullet = """||- **Rev. 472.** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `a48d198ffcb66ac00d0a8f2877339115d41d4805` (Rev. 471: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 471, §11 kompakt changelog 116–471, §12 updated; fixes: dokument PRD typo (dokeman), §13 stale refs, §12 range Rev. 468–471), 10 / 0 (10 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 471** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokumen PRD **REVISI** — rev 472 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 471; branch 10 ahead / 0 behind origin_main."""

# Find and remove the misplaced Rev. 472 bullet
malformed = "\n\n" + rev472_bullet
if rev472_bullet in content:
    content = content.replace(rev472_bullet, "")
    print("Removed misplaced Rev. 472 bullet from §8.1 section")
else:
    print("WARNING: Missed Rev. 472 bullet exact match")

# Also handle the case where the bullet might be concatenated with other text
# (the line 224 shows "...origin_main.spor NFC Tools →" — the bullet was concatenated)
# Let's search for the bullet pattern more loosely
import re
# Find the bullet that starts with "||- **Rev. 472.**" 
rev472_pattern = r'\n\n\|\|- \*\*Rev\. 472\*\*\. 24 Oktober 2026 \(WIB\): PRD fresh verification.*?origin_main\.spor NFC Tools'
content2, n = re.subn(rev472_pattern, '\n\n', content)
print(f"Removed via regex: {n}")
content = content2

# --- Step 3: Add Rev. 472 bullet after the §12 Rev. 471 bullet ---
# The §12 Rev. 471 bullet ends with: branch 8 ahead / 0 behind origin_main.
# Find the exact position of the §12 Rev. 471 bullet end
rev471_12_marker = "branch 8 ahead / 0 behind origin_main."
idx = content.find(rev471_12_marker)
if idx == -1:
    print("ERROR: Rev. 471 marker not found for §12")
else:
    # Find where the bullet ends (position after the marker)
    bullet_end = idx + len(rev471_12_marker)
    # Add Rev. 472 bullet after the §12 Rev. 471 bullet
    content = content[:bullet_end] + "\n" + rev472_bullet + content[bullet_end:]
    print("Added Rev. 472 bullet after §12 Rev. 471 bullet")

# --- Step 4: Verify changes ---
print(f"\nFinal checks:")
print(f"  'a48d198ffcb66ac00d0a8f2877339115d41d4805' in content: {'a48d198ffcb66ac00d0a8f2877339115d41d4805' in content}")
print(f"  'e1a192e2379eb8564610be398c72937f93bfd64d' in content: {'e1a192e2379eb8564610be398c72937f93bfd64d' in content}")
print(f"  'rev. 472' occurrences: {content.count('Rev. 472.')}")
print(f"  '10 commits ahead' occurrences: {content.count('10 commits ahead')}")
print(f"  'Rev. 116–472' in content: {'Rev. 116–472' in content}")
print(f"  'Rev. 468–472' in content: {'Rev. 468–472' in content}")

with open(PATH, 'w') as f:
    f.write(content)

print("\nDone.")
