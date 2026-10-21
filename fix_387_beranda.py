#!/usr/bin/env python3
"""Update Rev. 387 section's Beranda hardcode bullet to match actual files."""
import os

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD_PATH = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

old_beranda = """   - **Beranda hardcode:** `Beranda.tsx` (totalSantri count: 4) & `src/app/beranda/page.tsx` (totalSantri count: 3) — **belum fetch real-time dari DB**; tidak menggunakan nilai DB aktual."""

new_beranda = """   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded totalSantri (totalSantri: 453, totalGuru: 54, totalKelas: 18 — sesuai `dev.db`); belum fetch real-time dari DB; tidak menggunakan nilai DB aktual."""

if old_beranda in content:
    content = content.replace(old_beranda, new_beranda, 1)
    print("Rev. 387 Beranda hardcoded bullet updated")
else:
    print("WARNING: Rev. 387 Beranda bullet not found")

with open(PRD_PATH, "w", encoding="utf-8") as f:
    f.write(content)
print(f"PRD size: {os.path.getsize(PRD_PATH)} bytes")
