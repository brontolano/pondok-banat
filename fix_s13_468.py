#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the §13 Rev. 467 entry
marker = "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification"
idx = content.find(marker)
if idx < 0:
    print("ERROR: marker not found")
    exit(1)

# Find the end of this entry (next entry starts with "||- **Rev. 462.**")
end_marker = "||- **Rev. 462.**"
end_idx = content.find(end_marker, idx)
if end_idx < 0:
    end_idx = len(content)

# Build the new Rev. 468 entry
new_entry = (
    "||- **Rev. 468.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); "
    "HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); "
    "header Rev. 468, §11 kompakt changelog 116–467, §12 updated), "
    "5 / 0 (5 commits ahead origin_main). "
    "State stabil, tidak ada perubahan signifikan dari Rev. 467 (data terkonsisten). "
    "Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. "
    "Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. "
    "**M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). "
    "**Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). "
    "**Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). "
    "**Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. "
    "**Status:** dokeman PRD **REVISI** — rev 468 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 467; branch 5 ahead / 0 behind origin_main."
)

print(f"Replacing entry at {idx} to {end_idx} ({end_idx - idx} chars) with new entry ({len(new_entry)} chars)")

content = content[:idx] + new_entry + content[end_idx:]

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("File updated successfully.")
