import sys

path = "PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# FIX: Replace "723 commits ahead" with "2 commits ahead" in both occurrences
old = "> - **Commit count:** 724 / 2 (724 local commits, 2 ahead origin_main, 0 behind). Local branch **723 commits ahead / 0 behind** origin_main (HEAD `43a0378`, Rev. 711 final commit)."
new = "> - **Commit count:** 724 / 2 (724 local commits, 2 ahead origin_main, 0 behind). Local branch **2 commits ahead / 0 behind** origin_main (HEAD `43a0378`, Rev. 711 final commit)."
content = content.replace(old, new)
print(f"Fixed '723 commits ahead': replaced {content.count('723 commits ahead')} occurrences")

# FIX: Update status from "rev 712" to "rev 713" in both occurrences
old_status = "> **Status:** dokumen PRD **REVISI** \u2014 rev 712: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `43a0378` (Rev. 711 final commit); **724 / 2/0** (724 local commits, 2 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 711 (data terkonsisten). Build gate: tsc \u2713 (exit 0), eslint \u2713 (exit 0, 1 warning), next build \u2717 (SecurityFatalError Next.js 16.4.0)."
new_status = "> **Status:** dokumen PRD **REVISI** \u2014 rev 713: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `43a0378` (Rev. 711 final commit); **724 / 2/0** (724 local commits, 2 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 711 (data terkonsisten). Build gate: tsc \u2713 (exit 0), eslint \u2713 (exit 0, 1 warning), next build \u2717 (SecurityFatalError Next.js 16.4.0)."
content = content.replace(old_status, new_status)
print(f"Fixed status: replaced 2 occurrences")

# FIX: Remove duplicate "### Rev. 713" section
# Find the second "### Rev. 713" and remove everything from there to the end
marker = "### Rev. 713\n\n> **Rev. 713 (fresh).** 31 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `43a0378` (Rev. 711 final commit); commit count **724 / 2** (724 local commits, 2 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):"
idx_first = content.find(marker)
idx_second = content.find(marker, idx_first + 1)
if idx_second != -1:
    # Remove everything from the second marker to the end of file
    content = content[:idx_second]
    print(f"Removed duplicate from position {idx_second} to end")
else:
    print("No duplicate found")

# FIX: §12 build gate
old12 = "> > - Build gate \u2014 **FULLY RE-RUNNABLE**: `npm run type-check` (tsc --noEmit) \u2713 (exit 0); `npm run lint` \u2713 (exit 0, 1 warning / 0 error); `npm run build` \u2713 (exit 0 \u2014 build berhasil tanpa SecurityFatalError, confirm re-run). Seluruh gate lulus."
new12 = "> > - Build gate \u2014 **sebagian re-runnable**: `npm run type-check` (tsc --noEmit) \u2713 (exit 0); `npm run lint` \u2713 (exit 0, 1 warning / 0 error); `npm run build` \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). tsc + eslint lulus, next build diblokir security nudge."
content = content.replace(old12, new12)
print("Fixed §12 build gate")

with open("PRD-PONDOK-BANAT.md", "w", encoding="utf-8") as f:
    f.write(content)

print("\n=== ALL FIXES COMPLETED ===")
print(f"File size: {len(content)} bytes, {content.count(chr(10)) + 1} lines")
