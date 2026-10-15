import os, openpyxl

d = [e for e in os.listdir("/opt/data/home/workspace/dev/pondok-banat") if e.startswith(".data")][0]
p = os.path.join("/opt/data/home/workspace/dev/pondok-banat", d, "DATA PARA PENGAJAR BANAT.xlsx")
wb = openpyxl.load_workbook(p, read_only=True)

print("=== TAHUN 2026-2027 sheet ===")
ws = wb["TAHUN 2026-2027"]
rows = list(ws.iter_rows(values_only=True))
# print header + 5 data rows
for r in rows[:7]:
    print(r)
# count non-empty rows
data = [r for r in rows if any(c is not None and str(c).strip() for c in r)]
print("total non-empty rows:", len(data))

print("\n=== Table 1 sheet ===")
ws2 = wb["Table 1"]
rows2 = list(ws2.iter_rows(values_only=True))
data2 = [r for r in rows2 if any(c is not None and str(c).strip() for c in r)]
print("total non-empty rows:", len(data2))
for r in data2[:5]:
    print(r)
wb.close()
