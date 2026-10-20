import re

with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# === 1. HEADER REPLACEMENTS ===
# 1a. Rev. 269 -> Rev. 270 (header)
content = content.replace(
    '> **Rev. 269 — 18 Oktober 2026 (WIB).',
    '> **Rev. 270 — 18 Oktober 2026 (WIB).'
)

# 1b. Git HEAD reference in header
content = content.replace(
    'Git HEAD: `5cf80a0c810c517d11b6ebc0aa909ab10864abae` (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `5cf80a0c810c517d11b6ebc0aa909ab10864abae`)',
    'Git HEAD: `342ede6926c0064539bf43eba8dc6639b895c827` (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `342ede6926c0064539bf43eba8dc6639b895c827`)'
)

# 1c. revisi terbaru = Rev. 268 -> Rev. 269 (header)
content = content.replace(
    'revisi terbaru = Rev. 268, sudah dicomit',
    'revisi terbaru = Rev. 269, sudah dicomit'
)

# 1d. HEAD = 5cf80a0c -> HEAD = 342ede6 (header)
content = content.replace(
    'HEAD = `5cf80a0c810c517d11b6ebc0aa909ab10864abae`',
    'HEAD = `342ede6926c0064539bf43eba8dc6639b895c827`'
)

# 1e. Branch 18 -> Branch 19 (header)
content = content.replace(
    'Branch 18 commit ahead',
    'Branch 19 commit ahead'
)

print("After header replacements:")
print('  Rev. 269 count:', content.count('Rev. 269'))
print('  Rev. 270 count:', content.count('Rev. 270'))
print('  5cf80a0 count:', content.count('5cf80a0c810c517d11b6ebc0aa909ab10864abae'))
print('  342ede6 count:', content.count('342ede6926c0064539bf43eba8dc6639b895c827'))
print('  18 commit count:', content.count('18 commit'))
print('  19 commit count:', content.count('19 commit'))

# === 2. SECTION 47 -> 48 REPLACEMENTS ===
# 2a. Section title
content = content.replace(
    '## 47. REVISI TERBARU (Rev. 269 — 18 Oktober 2026 WIB)',
    '## 48. REVISI TERBARU (Rev. 270 — 18 Oktober 2026 WIB)'
)

# 2b. "Tidak ada perubahan signifikan dari Rev. 268"
content = content.replace(
    'state stabil. Tidak ada perubahan signifikan dari Rev. 268 (data terkonsisten)',
    'state stabil. Tidak ada perubahan signifikan dari Rev. 269 (data terkonsisten)'
)

# 2c. Git HEAD (local) in section
content = content.replace(
    'Git HEAD (local):** `5cf80a0c810c517d11b6ebc0aa909ab10864abae` "Rev. 268: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 268 + added section 46" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `5cf80a0c810c517d11b6ebc0aa909ab10864abae`). Local branch **18** commit ahead dari `origin/main` (`45d33ef348b11ae49789224687913adeb01d1842` = Rev. 250).',
    'Git HEAD (local):** `342ede6926c0064539bf43eba8dc6639b895c827` "Rev. 269: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 269 + added section 47" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `342ede6926c0064539bf43eba8dc6639b895c827`). Local branch **19** commit ahead dari `origin/main` (`45d33ef348b11ae49789224687913adeb01d1842` = Rev. 250).'
)

# 2d. Local branch 18 commit ahead (second occurrence, inside git head line)
content = content.replace(
    'Local branch 18 commit ahead',
    'Local branch 19 commit ahead'
)

# 2e. Branch-ahead: 18 commit
content = content.replace(
    '**Branch-ahead:** 18 commit (Rev. 251 + Rev. 252 + ... + Rev. 260, Rev. 261, Rev. 262, Rev. 263, Rev. 264, Rev. 265, Rev. 266, Rev. 267, Rev. 268; seluruh commit lokal belum dipush ke origin; `git rev-list --count origin/main..HEAD` = 18)',
    '**Branch-ahead:** 19 commit (Rev. 251 + Rev. 252 + ... + Rev. 260, Rev. 261, Rev. 262, Rev. 263, Rev. 264, Rev. 265, Rev. 266, Rev. 267, Rev. 268, Rev. 269; seluruh commit lokal belum dipush ke origin; `git rev-list --count origin/main..HEAD` = 19)'
)

# 2f. Branch-ahead count: diperbarui dari 17 -> 18 -> 19
content = content.replace(
    '**Branch-ahead count:** diperbarui dari 17 → 18 commit (`git rev-list --count origin/main..HEAD` = 18)',
    '**Branch-ahead count:** diperbarui dari 18 → 19 commit (`git rev-list --count origin/main..HEAD` = 19)'
)

# 2g. "rev 269 = verifikasi fresh ulang" -> "rev 270 = verifikasi fresh ulang"
content = content.replace(
    'rev 269 = verifikasi fresh ulang & konfirmasi stabilitas',
    'rev 270 = verifikasi fresh ulang & konfirmasi stabilitas'
)

# 2h. "Header PRD diperbarui ke **Rev. 269**" -> "Rev. 270"
content = content.replace(
    'Header PRD diperbarui ke **Rev. 269**',
    'Header PRD diperbarui ke **Rev. 270**'
)

# But we need to add the new "Perubahan dari Rev. 269" section before the Status line.
# First, find the exact text of the Status line start
old_status = '3. **Status:** dokumen PRD **REVISI** — rev 269 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 269**.'

# Remove the old Status line
content = content.replace(
    '3. **Status:** dokumen PRD **REVISI** — rev 269 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 269**.',
    '3. **Status:** dokumen PRD **REVISI** — rev 270 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 270**.'
)

# Now add the "Perubahan dari Rev. 269" section before the Status line
# The "Perubahan dari Rev. 268" section ends with:
old_perubahan268_end = '**Branch-ahead count:** diperbarui dari 17 → 18 commit (`git rev-list --count origin/main..HEAD` = 18).\n\n3. **Status:**'

# New content for Perubahan dari Rev. 269
new_perubahan269 = '''**Branch-ahead count:** diperbarui dari 18 → 19 commit (`git rev-list --count origin/main..HEAD` = 19).

3. **Perubahan dari Rev. 269:**
   - **Header PRD:** diperbarui ke **Rev. 270** (tanggal 18 Oktober 2026 WIB).
   - **New Section 48 (Rev. 270):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 270.
   - **Git HEAD di header:** diperbaiki dari `5cf80a0c810c517d11b6ebc0aa909ab10864abae` → `342ede6926c0064539bf43eba8dc6639b895c827` (aktual, sesuai HEAD commit Rev. 269).
   - **Branch-ahead count:** diperbarui dari 18 → 19 commit (`git rev-list --count origin/main..HEAD` = 19).

4. **Status:** dokumen PRD **REVISI** — rev 270 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 270**.'''

# Insert the new Perubahan from Rev. 269 section after the Perubahan dari Rev. 268 section
# We need to find the end of Perubahan dari Rev. 268 and insert before Status
# The Perubahan dari Rev. 268 section ends with: "Branch-ahead count:** diperbarui dari 17 → 18 commit (`git rev-list --count origin/main..HEAD` = 18)."
# Then there's a blank line, then "3. **Status:**"

# First, revert the status replacement we just did (we'll handle it manually)
# Actually, let me redo this more carefully.

# The current content after step 2g has:
# "3. **Status:** dokumen PRD **REVISI** — rev 270 = verifikasi fresh ulang & konfirmasi stabilitas; ... Header PRD diperbarui ke **Rev. 270**."
# We need to add the Perubahan dari Rev. 269 section between Perubahan dari Rev. 268 and Status.

# Find the end of Perubahan dari Rev. 268
old_delimiter = '**Branch-ahead count:** diperbarui dari 17 → 18 commit (`git rev-list --count origin/main..HEAD` = 18).\n\n3. **Status:**'

new_delimiter = '''**Branch-ahead count:** diperbarui dari 18 → 19 commit (`git rev-list --count origin/main..HEAD` = 19).

3. **Perubahan dari Rev. 269:**
   - **Header PRD:** diperbarui ke **Rev. 270** (tanggal 18 Oktober 2026 WIB).
   - **New Section 48 (Rev. 270):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas Rev. 270.
   - **Git HEAD di header:** diperbaiki dari `5cf80a0c810c517d11b6ebc0aa909ab10864abae` → `342ede6926c0064539bf43eba8dc6639b895c827` (aktual, sesuai HEAD commit Rev. 269).
   - **Branch-ahead count:** diperbarui dari 18 → 19 commit (`git rev-list --count origin/main..HEAD` = 19).

4. **Status:** dokumen PRD **REVISI** — rev 270 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 270**.'''

content = content.replace(old_delimiter, new_delimiter)

print("\nAfter section replacements:")
print('  Rev. 268 count:', content.count('Rev. 268'))
print('  Rev. 269 count:', content.count('Rev. 269'))
print('  Rev. 270 count:', content.count('Rev. 270'))
print('  5cf80a0 count:', content.count('5cf80a0c810c517d11b6ebc0aa909ab10864abae'))
print('  342ede6 count:', content.count('342ede6926c0064539bf43eba8dc6639b895c827'))
print('  18 commit count:', content.count('18 commit'))
print('  19 commit count:', content.count('19 commit'))

# Save
with open('PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print("\nFile saved successfully.")
