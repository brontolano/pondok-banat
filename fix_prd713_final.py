import sys

path = "PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

def replace(old, new, label, required=True):
    global content
    count = content.count(old)
    if required and count == 0:
        print(f"ERROR: '{label}' not found — aborting")
        sys.exit(1)
    content = content.replace(old, new)
    print(f"{label}: replaced {count} occurrence(s)")

# FIX 1: Header build gate
old1 = "Build gate: npm run type-check (tsc --noEmit) \u2717 (blocked \u2014 security scan); npm run lint \u2717 (blocked \u2014 security scan); npm run build (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate TIDAK RE-RUNNABLE \u2014 tsc, eslint, dan next build diblokir (security scan). Working tree: PRD synced ke Rev. 713;"
new1 = "Build gate: npm run type-check (tsc --noEmit) \u2713 (exit 0); npm run lint \u2713 (exit 0, 1 warning / 0 error); npm run build (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable \u2014 tsc + eslint lulus, next build diblokir security nudge. Working tree: PRD synced ke Rev. 713;"
replace(old1, new1, "Fix 1: header build gate", required=True)

# FIX 2: §11 intro commit count
old2 = "> - **Commit count:** 721 / 17/0 (721 local commits, 17 ahead origin_main, 0 behind). Local branch **721 commits ahead / 0 behind** origin_main. **origin/main:** `1e0486d` (Rev. 692, 0 behind)."
new2 = "> - **Commit count:** 724 / 2/0 (724 local commits, 2 ahead origin_main, 0 behind). Local branch **2 commits ahead / 0 behind** origin_main. **origin/main:** `04ce9b7` (Rev. 712 final commit)."
replace(old2, new2, "Fix 2: §11 intro commit count", required=True)

# FIX 3: §11 intro working tree
old3 = "> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 708, commit d0615b5b2ddfec094afaac0e4b248c66687e7677); seluruh file lain cocak dengan HEAD; untracked: 51 (helper scripts); `git ls-files` = 268 files."
new3 = "> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 713, commit 04ce9b7); seluruh file lain cocak dengan HEAD; untracked: 56 (helper scripts); `git ls-files` = 268 files."
replace(old3, new3, "Fix 3: §11 intro working tree", required=True)

# FIX 4: §11 intro build gate
old4 = "> - **Build gate:** `npm run type-check` (tsc --noEmit) \u2713 (exit 0) \u2014 **PASS**; `npm run lint` \u2713 (exit 0, 1 warning / 0 error) \u2014 **PASS**; `npx next build` \u2713 (exit 0 \u2014 build berhasil tanpa SecurityFatalError, next build berhasil tanpa SecurityFatalError) \u2014 **PASS**. Build gate **FULLY RE-RUNNABLE** \u2014 seluruh gate lulus. `node_modules` present (5103 dirs / 84021 files)."
new4 = "> - **Build gate:** `npm run type-check` (tsc --noEmit) \u2713 (exit 0) \u2014 **PASS**; `npm run lint` \u2713 (exit 0, 1 warning / 0 error) \u2014 **PASS**; `npx next build` \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability) \u2014 **FAIL**. Build gate **sebagian re-runnable** \u2014 tsc + eslint lulus, next build diblokir security nudge. `node_modules` present (5103 dirs / 84021 files)."
replace(old4, new4, "Fix 4: §11 intro build gate", required=True)

# FIX 5: §11 intro status
old5 = "> **Status:** dokumen PRD **REVISI** \u2014 rev 709: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `d0615b5b2ddfec094afaac0e4b248c66687e7677` (Rev. 708 final commit); **720 / 16/0** (720 local commits, 16 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 708 (data terkonsisten)."
new5 = "> **Status:** dokumen PRD **REVISI** \u2014 rev 713: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `04ce9b7` (Rev. 712 final commit); **724 / 2/0** (724 local commits, 2 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 712 (data terkonsisten)."
replace(old5, new5, "Fix 5: §11 intro status", required=True)

# FIX 6: §12 build gate
old6 = "> > - Build gate \u2014 **FULLY RE-RUNNABLE**: `npm run type-check` (tsc --noEmit) \u2713 (exit 0); `npm run lint` \u2713 (exit 0, 1 warning / 0 error); `npm run build` \u2713 (exit 0 \u2014 build berhasil tanpa SecurityFatalError, confirm re-run). Seluruh gate lulus."
new6 = "> > - Build gate \u2014 **sebagian re-runnable**: `npm run type-check` (tsc --noEmit) \u2713 (exit 0); `npm run lint` \u2713 (exit 0, 1 warning / 0 error); `npm run build` \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). tsc + eslint lulus, next build diblokir security nudge."
replace(old6, new6, "Fix 6: §12 build gate", required=True)

# FIX 7: Rev. 711 section commit count - "723 commits ahead" -> "2 commits ahead"
old7 = "> - **Commit count:** 724 / 2 (724 local commits, 2 ahead origin_main, 0 behind). Local branch **723 commits ahead / 0 behind** origin_main (HEAD `43a0378`, Rev. 711 final commit)."
new7 = "> - **Commit count:** 724 / 2 (724 local commits, 2 ahead origin_main, 0 behind). Local branch **2 commits ahead / 0 behind** origin_main (HEAD `43a0378`, Rev. 711 final commit)."
replace(old7, new7, "Fix 7: Rev. 711 commit count", required=True)

# FIX 8: Rev. 713 section commit count (both occurrences at lines 1429 and 1446)
old8a = "> - **Commit count:** 724 / 2 (724 local commits, 2 ahead origin_main, 0 behind). Local branch **723 commits ahead / 0 behind** origin_main (HEAD `43a0378`, Rev. 711 final commit).\n>\n> **Status:** dokumen PRD **REVISI** \u2014 rev 712: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `43a0378` (Rev. 711 final commit); **724 / 2/0** (724 local commits, 2 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 711 (data terkonsisten). Build gate: tsc \u2713 (exit 0), eslint \u2713 (exit 0, 1 warning), next build \u2717 (SecurityFatalError Next.js 16.4.0).\n\n\n### Rev. 713"
new8a = "> - **Commit count:** 724 / 2 (724 local commits, 2 ahead origin_main, 0 behind). Local branch **2 commits ahead / 0 behind** origin_main (HEAD `43a0378`, Rev. 711 final commit).\n>\n> **Status:** dokumen PRD **REVISI** \u2014 rev 713: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `43a0378` (Rev. 711 final commit); **724 / 2/0** (724 local commits, 2 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 711 (data terkonsisten). Build gate: tsc \u2713 (exit 0), eslint \u2713 (exit 0, 1 warning), next build \u2717 (SecurityFatalError Next.js 16.4.0).\n\n\n### Rev. 713"
replace(old8a, new8a, "Fix 8a: Rev. 713 section (first) commit count + status", required=True)

# FIX 9: Remove duplicate "### Rev. 713" section
# Find the second "### Rev. 713" and remove everything from there to the next "### Rev." or end
marker = "### Rev. 713\n\n> **Rev. 713 (fresh).** 31 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `43a0378` (Rev. 711 final commit); commit count **724 / 2** (724 local commits, 2 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):"
idx_first = content.find(marker)
idx_second = content.find(marker, idx_first + 1)
if idx_second == -1:
    print("Fix 9: no duplicate found")
else:
    # Find the end of the second duplicate section - look for the next "### Rev." or end of file
    idx_next_section = content.find("### Rev.", idx_second + 1)
    if idx_next_section == -1:
        idx_next_section = len(content)
    else:
        # Go back to the start of that line
        while idx_next_section > 0 and content[idx_next_section - 1] != '\n':
            idx_next_section -= 1
    print(f"Fix 9: removing duplicate from {idx_second} to {idx_next_section}")
    content = content[:idx_second] + content[idx_next_section:]
    print("Fix 9: duplicate removed OK")

# FIX 10: §12 build gate
old10 = "> > - Build gate \u2014 **FULLY RE-RUNNABLE**: `npm run type-check` (tsc --noEmit) \u2713 (exit 0); `npm run lint` \u2713 (exit 0, 1 warning / 0 error); `npm run build` \u2713 (exit 0 \u2014 build berhasil tanpa SecurityFatalError, confirm re-run). Seluruh gate lulus."
new10 = "> > - Build gate \u2014 **sebagian re-runnable**: `npm run type-check` (tsc --noEmit) \u2713 (exit 0); `npm run lint` \u2713 (exit 0, 1 warning / 0 error); `npm run build` \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). tsc + eslint lulus, next build diblokir security nudge."
replace(old10, new10, "Fix 10: §12 build gate", required=True)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("\n=== ALL FIXES COMPLETED ===")
print(f"File size: {len(content)} bytes, {content.count(chr(10)) + 1} lines")
