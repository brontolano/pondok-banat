import openpyxl
from collections import Counter

f2 = '.data-pondokbanat/Data Banat 2026-2027.xlsx'
wb2 = openpyxl.load_workbook(f2, read_only=True)

# Data Kelas structure
ws2 = wb2['Data Kelas']
rows2 = list(ws2.iter_rows(values_only=True))
print('=== Data Kelas rows:', len(rows2))
print('Row 1 (header):', rows2[1])
print('Row 2 (first):', rows2[2])

# Determine sections from header row
header = rows2[1]
print('Non-None header values:', [h for h in header if h is not None])

# Also check column count: Data Kelas has 98 rows; skip header+blank
# Get section labels: columns after Takhosus/Tamhidi
# Header: TAKHOSUS(col0), None(col1), TAMHIDI A(col4), TAMHIDI B(col8), 1A(col12)...
# Data is 5 per class group
# Sections to count: 1A,1B,2A,2B,3A,3B (6) + Tamhidi A + Tamhidi B (2) + Takhosus (1)
# = 9 sections

# Count students per class section for verification
# Row 3 onward: 5 students per section group
# Print row 3
print('Row 3:', rows2[3])

# Takhosil/Tamhidi/1-3 sections
print('=== Check section columns in header ===')
header_vals = [(i, v) for i, v in enumerate(header) if v is not None]
print(header_vals)
