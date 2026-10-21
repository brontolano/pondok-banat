PATH = "PRD-PONDOK-BANAT.md"
with open(PATH, "r", encoding="utf-8") as f:
    src = f.read()

# Fix 1: Remove duplicate build gate note in header
old_dup = "Build quality gate: NO LONGER RE-RUNABLE (node_modules absen; .next partial) (node_modules absen; .next partial) — node_modules/absent"
new_dup = "Build quality gate: NO LONGER RE-RUNABLE (node_modules absen; .next partial) — node_modules/absent"
count = src.count(old_dup)
if count == 1:
    src = src.replace(old_dup, new_dup)
    print("Fixed header duplicate build gate note")
else:
    print(f"Header duplicate not found, count={count}")

# Fix 2: Update "Perubahan dari Rev. 370" in section 156
old_156 = """2. **Perubahan dari Rev. 370:**
   - **Header PRD:** diperbarui ke **Rev. 371** (tanggal 20 Oktober 2026 WIB).
   - **Git HEAD (local):** `9f679a030095d8827c246c104b2a97429c0144f9` (Rev. 370, commit `9f679a030095d8827c246c104b2a97429c0144f9`); origin/main = `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). Branch **2 commits ahead** origin.main.
   - **Git ls-files:** 152 file; 4 file tidak ter-track.
   - **dev.db:** absent (dihapus oleh commit HEAD "Release: clean core files only" 1dc891d); rekonstruksi seed diperlukan.
   - **Build quality gate:** NO LONGER RE-RUNABLE (node_modules/absent; .next partial).
   - **Schema:** 17 model terdefinisi (KitabProgress, Sertakan, uidNfc semua ada), `prisma validate` tidak dapat dijalankan karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26-28) & `src/app/beranda/page.tsx` (baris 14-16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB; sudah diperbarui ke 453 sesuai data Excel grade sheets)."""

new_156 = """2. **Perubahan dari Rev. 370:**
   - **Header PRD:** diperbarui ke **Rev. 371** (tanggal 20 Oktober 2026 WIB).
   - **Git HEAD (local):** `872ed45a8bbffd2b524eb1840edfac833b616f00` (Rev. 371, commit `872ed45a8bbffd2b524eb1840edfac833b616f00`); origin/main = `d52f63c0f55cd1a507b75e2de8ae6ff5e5bf9a72` (Rev. 368). Local branch **3 commits ahead** origin.main (naik dari 2 commits sebelumnya).
   - **Git ls-files:** 152 file; 6 file tidak ter-track.
   - **dev.db:** absent (dihapus oleh commit HEAD "Release: clean core files only" 1dc891d); rekonstruksi seed diperlukan.
   - **Build quality gate:** NO LONGER RE-RUNABLE (node_modules/absent; .next partial).
   - **Schema:** 17 model terdefinisi (KitabProgress, Sertakan, uidNfc semua ada), `prisma validate` tidak dapat dijalankan karena `prisma` CLI tidak terinstall (`node_modules` absen).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok Banat); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26-28) & `src/app/beranda/page.tsx` (baris 14-16) masih hardcode `totalSantri: 453, totalGuru: 54, totalKelas: 18` (bukan fetch real-time dari DB; sudah diperbarui ke 453 sesuai data Excel grade sheets)."""

count2 = src.count(old_156)
if count2 == 1:
    src = src.replace(old_156, new_156)
    print("Fixed section 156 Perubahan dari Rev. 370")
else:
    print(f"Section 156 Perubahan not found, count={count2}")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(src)

print("New file size:", len(src))
