import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Print lines 539-540 (0-indexed: 538-539) with exact repr
for i in [538, 539]:
    line = lines[i]
    print(f"Index {i}: {repr(line[:120])}")
    print(f"  Contains '|| 652': {'|| 652' in line}")
    print(f"  Contains '|||': {'|||' in line}")
    print()
