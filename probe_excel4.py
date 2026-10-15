import os, openpyxl

base = "/opt/data/home/workspace/dev/pondok-banat"
d = [e for e in os.listdir(base) if e.startswith(".data")][0]
data_dir = os.path.join(base, d)
print("folder:", repr(d))

for f in ["DATA PARA PENGAJAR BANAT.xlsx", "Data Banat 2026-2027.xlsx", "Data Nilai Semester 1 TA 2026_2027.xlsx"]:
    p = os.path.join(data_dir, f)
    print("===", f, "===")
    wb = openpyxl.load_workbook(p, read_only=True)
    for sh in wb.sheetnames:
        ws = wb[sh]
        rows = list(ws.iter_rows(values_only=True))
        # trim trailing empty rows
        while rows and all(c is None for c in rows[-1]):
            rows.pop()
        print("  sheet '%s': %d rows (max col %d)" % (sh, len(rows), len(rows[0]) if rows else 0))
        for r in rows[:2]:
            print("    ", r)
    wb.close()
    print()
