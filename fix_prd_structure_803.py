import sys

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the Rev. 803 section that was inserted in the wrong place
# The Rev. 803 section starts with "### Rev. 803" and ends with the blank line after "Schema inconsistency (Rev. 38–45) SELESAI."
rev803_start = content.find("### Rev. 803")
rev803_end = content.find("### Rev. 804")  # placeholder, will search for next section

# Find the end of the Rev. 803 section
# The Rev. 803 section ends with:
# > - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI.
# \n\n
# (this blank line is after the Rev. 803 content)
rev803_marker = """> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI.
"""

if rev803_marker in content[rev803_start:]:
    rev803_content_start = rev803_start
    rev803_content_end = rev803_start + content[rev803_start:].find(rev803_marker) + len(rev803_marker)
    rev803_section = content[rev803_content_start:rev803_content_end]
    print("Found Rev. 803 section at position", rev803_content_start, "to", rev803_content_end)
    print("Rev. 803 section length:", len(rev803_section))
else:
    print("Rev. 803 marker not found")
    sys.exit(1)

# Find the orphaned Rev. 802 content that was left behind
# The orphaned content starts with " (824 local commits, 16 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 801 (data terkonsisten)."
orphaned_start = content.find(" (824 local commits, 16 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 801 (data terkonsisten).")

# The orphaned content ends with the duplicate Rev. 801 Status line
orphaned_end_marker = """> - **Status:** dokumen PRD **REVISI** — rev 801: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `37dc5c7` (Rev. 800 committed); **822 / 14/0** (822 local commits, 14 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 800 (data terkonsisten)."""

if orphaned_end_marker in content:
    orphaned_end = content.find(orphaned_end_marker) + len(orphaned_end_marker)
    print("Found orphaned Rev. 802 content at position", rev803_content_end, "to", orphaned_end)
    orphaned_section = content[rev803_content_end:orphaned_end]
    print("Orphaned section length:", len(orphaned_section))
else:
    print("Orphaned Rev. 801 Status marker not found")
    sys.exit(1)

# Remove both the Rev. 803 section and the orphaned content
content = content[:rev803_content_start] + content[rev803_content_end:]
content = content[:orphaned_start] + content[orphaned_end:]

# Now insert Rev. 803 after the Rev. 802 section (after the duplicate Rev. 801 Status line)
# The duplicate Rev. 801 Status line ends at orphaned_end (which we already consumed)
# So we insert after that position

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Removed Rev. 803 from wrong position and orphaned content")
print("Done. New file length:", len(content))
