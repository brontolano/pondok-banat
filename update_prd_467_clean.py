#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean update: start from git HEAD (Rev. 466), apply all changes to Rev. 467.
Source: /tmp/prd_orig_466.md (original git HEAD file, 792 lines).
"""
import io

src = "/tmp/prd_orig_466.md"
dst = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(src, "r", encoding="utf-8") as f:
    content = f.read()

original = content
changes = []

def replace_once(old, new, label, content):
    if old in content:
        content = content.replace(old, new, 1)
        changes.append(f"[{label}] OK")
        return content
    else:
        changes.append(f"[{label}] FAIL (not found)")
        return content

# ── 1. HEADER ──────────────────────────────────────────────────────────────
content = replace_once(
    "Rev. 466: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 466, §11 kompakt changelog 116–465",
    "Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466",
    "1.HEADER",
    content,
)

# ── 2. §11 HEADER ──────────────────────────────────────────────────────────
content = replace_once(
    "## 11. REVISI TERBARU (Rev. 463 — 23 Oktober 2026 WIB)",
    "## 11. REVISI TERBARU (Rev. 467 — 23 Oktober 2026 WIB)",
    "2.§11HEADER",
    content,
)

# ── 3. §11: insert new entry for Rev. 467 after §11 header ─────────────────
# Find the §11 header, then insert the new entry right after
s11_header = "## 11. REVISI TERBARU (Rev. 467 — 23 Oktober 2026 WIB)"
s11_entry = (
    "\n"
    "||\n"
    "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main.\n"
)
content = replace_once(s11_header, s11_header + s11_entry, "3.§11INSERT", content)

# ── 4. §12 HEADER ──────────────────────────────────────────────────────────
content = replace_once(
    "## 12. REVISI TERBARU (Rev. 463 — 23 Oktober 2026 WIB)",
    "## 12. REVISI TERBARU (Rev. 467 — 23 Oktober 2026 WIB)",
    "4.§12HEADER",
    content,
)

# ── 5. §12 content ─────────────────────────────────────────────────────────
# 5a. Line 759: state stabil comparison
content = replace_once(
    "state stabil. Tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten).**",
    "state stabil. Tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten).**",
    "5a.LINE759",
    content,
)

# 5b. Line 760: branch status
content = replace_once(
    "Local branch **0 commit ahead / 0 behind** origin_main (in sync)",
    "Local branch **4 commits ahead / 0 behind** origin_main",
    "5b.LINE760A",
    content,
)

# 5c. Line 760: 0/0 → 4/0
content = replace_once(
    "updated), 0 / 0 (0 commit ahead origin_main). Local branch",
    "updated), 4 / 0 (4 commits ahead origin_main). Local branch",
    "5c.LINE760B",
    content,
)

# 5d. Line 760: header Rev. 463 → Rev. 467
content = replace_once(
    "header Rev. 463, §11 kompakt changelog 116–462, §12 updated",
    "header Rev. 467, §11 kompakt changelog 116–466, §12 updated",
    "5d.LINE760C",
    content,
)

# 5e. Line 761: revision label
content = replace_once(
    "revisi terbaru = Rev. 463",
    "revisi terbaru = Rev. 467",
    "5e.LINE761A",
    content,
)

# 5f. Line 761: HEAD hash + Rev. 467
content = replace_once(
    "HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463)",
    "HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467)",
    "5f.LINE761B",
    content,
)

# 5g. Line 770: rev label
content = replace_once(
    "rev 463 = PRD fresh verification & stability confirmation",
    "rev 467 = PRD fresh verification & stability confirmation",
    "5g.LINE770A",
    content,
)

# 5h. Line 770: HEAD hash + Rev. 467
content = replace_once(
    "HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463), 0 / 0",
    "HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467), 4 / 0",
    "5h.LINE770B",
    content,
)

# 5i. Line 770: comparison
content = replace_once(
    "tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten)",
    "tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)",
    "5i.LINE770C",
    content,
)

# ── 6. §13: change Rev. 463 entry to Rev. 467 ──────────────────────────────
# The §13 Rev. 463 entry is the reference table entry for the original Rev. 463.
# Change its header to Rev. 467, update hash, 0/0→4/0, comparison, and label.
orig_s13_463 = (
    "|||- **Rev. 463.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 463, §11 kompakt changelog 116–462, §12 updated), 0 / 0 (0 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten). Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 463 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 462; branch 0 ahead / 0 behind origin_main."
)
new_s13_467 = (
    "|||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main."
)
content = replace_once(orig_s13_463, new_s13_467, "6.§13REV463→467", content)

# ── 7. Verify all replacements succeeded ────────────────────────────────────
print("=== Changes applied ===")
for c in changes:
    print(c)
print(f"\nTotal changes: {len(changes)}")
print(f"All successful: {all('OK' in c for c in changes)}")

# ── 8. Write output ─────────────────────────────────────────────────────────
with io.open(dst, "w", encoding="utf-8") as f:
    f.write(content)

# Count lines
line_count = content.count("\n") + 1
print(f"\nOutput written to {dst}")
print(f"Total lines: {line_count}")
