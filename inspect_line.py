with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Line 437 (0-indexed: 436)
line = lines[436]
print("LENGTH:", len(line))
print("FIRST 200:", repr(line[:200]))
print("LAST 200:", repr(line[-200:]))
print("TRIM LESS 80:", repr(line[80:len(line)-80]))
