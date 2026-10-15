import openpyxl, os
from collections import OrderedDict

base = "/opt/data/home/workspace/dev/pondok-banat/.data-pondokbanat"
pdfdir = os.path.join(base, "Pdf had mata pelajaran")

# Count PDF-like files in Pdf folder
all_files = []
for root, dirs, files in os.walk(pdfdir):
    for fn in files:
        all_files.append(os.path.relpath(os.path.join(root, fn), base))
print("=== PDF files in Pdf folder ===")
for fn in sorted(all_files):
    print("   ", fn)
print("TOTAL:", len(all_files))

# Classify: RPP vs SILABUS by filename
rp = [f for f in all_files if "rpp" in f.lower() or "rpp" in f.lower()]
sil = [f for f in all_files if "silabus" in f.lower()]
print("RPP files:", len(rp), rp)
print("SILABUS files:", len(sil), sil)

# Unique subjects: parse Mata Pelajaran sheet, exclude structural tokens
wb2 = openpyxl.load_workbook(os.path.join(base, "Data Banat 2026-2027.xlsx"), read_only=True)
ws2 = wb2["Mata Pelajaran"]
mrows = list(ws2.iter_rows(values_only=True))
struct = {"NO", "MATA PELAJARAN", "Pengajar", "JP", "KELAS 4", "KELAS 5", "KELAS 6", "", "None"}
subjects = OrderedDict()
for r in mrows[2:]:
    for c in r:
        if c is None:
            continue
        s = str(c).strip()
        if s in struct or s.isdigit():
            continue
        subjects[s] = True
print("=== Unique SUBJECT names (Mata Pelajaran) ===")
print("Count:", len(subjects))
for s in sorted(subjects):
    print("   -", s)
wb2.close()
