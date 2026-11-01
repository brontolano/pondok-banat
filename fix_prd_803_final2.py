import sys

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# The duplicate Rev. 802 section starts with "> ### Rev. 802" (nested, with > prefix)
# and ends with the duplicate Rev. 801 Status line "> - **Status:** dokumen PRD **REVISI** — rev 801: ..."

duplicate_start = "> ### Rev. 802\n"
duplicate_end = """> - **Status:** dokumen PRD **REVISI** — rev 801: PRD fresh verification & stability confirmation (cron run, 31 Oktober 2026 (WIB)); HEAD `37dc5c7` (Rev. 800 committed); **822 / 14/0** (822 local commits, 14 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 800 (data terkonsisten)."""

if duplicate_start in content:
    start_pos = content.find(duplicate_start)
    if duplicate_end in content[start_pos:]:
        end_pos = start_pos + content[start_pos:].find(duplicate_end) + len(duplicate_end)
        duplicate_section = content[start_pos:end_pos]
        print("Found duplicate Rev. 802 section at position", start_pos, "to", end_pos)
        print("Duplicate section length:", len(duplicate_section))
        
        # Remove the duplicate
        content = content[:start_pos] + content[end_pos:]
        print("Removed duplicate Rev. 802 section")
    else:
        print("Duplicate end marker not found")
else:
    print("Duplicate Rev. 802 start marker not found")
    sys.exit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Done. New file length:", len(content))
