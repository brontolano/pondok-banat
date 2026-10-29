import sys

path = "PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# FIX: Header build gate - update to match actual verification
old = "Build gate: npm run type-check (tsc --noEmit) \u2717 (blocked \u2014 security scan); npm run lint \u2717 (blocked \u2014 security scan); npm run build (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate TIDAK RE-RUNNABLE \u2014 tsc, eslint, dan next build diblokir (security scan). Working tree: PRD synced ke Rev. 713;"
new = "Build gate: npm run type-check (tsc --noEmit) \u2713 (exit 0); npm run lint \u2713 (exit 0, 1 warning / 0 error); npm run build (next build) \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable \u2014 tsc + eslint lulus, next build diblokir security nudge. Working tree: PRD synced ke Rev. 713;"
content = content.replace(old, new)
print(f"Fixed header build gate: {1 if old in content else 'already done'}")

# FIX: §11 intro build gate
old2 = "> - **Build gate:** `npm run type-check` (tsc --noEmit) \u2713 (exit 0) \u2014 **PASS**; `npm run lint` \u2713 (exit 0, 1 warning / 0 error) \u2014 **PASS**; `npx next build` \u2713 (exit 0 \u2014 build berhasil tanpa SecurityFatalError, next build berhasil tanpa SecurityFatalError) \u2014 **PASS**. Build gate **FULLY RE-RUNNABLE** \u2014 seluruh gate lulus. `node_modules` present (5103 dirs / 84021 files)."
new2 = "> - **Build gate:** `npm run type-check` (tsc --noEmit) \u2713 (exit 0) \u2014 **PASS**; `npm run lint` \u2713 (exit 0, 1 warning / 0 error) \u2014 **PASS**; `npx next build` \u2717 (exit 1 \u2014 SecurityFatalError: Next.js 16.4.0 has a known security vulnerability) \u2014 **FAIL**. Build gate **sebagian re-runnable** \u2014 tsc + eslint lulus, next build diblokir security nudge. `node_modules` present (5103 dirs / 84021 files)."
content = content.replace(old2, new2)
print(f"Fixed §11 intro build gate: {1 if old2 in content else 'already done'}")

with open("PRD-PONDOK-BANAT.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
