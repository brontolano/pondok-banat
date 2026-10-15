with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Line 437 (0-indexed 436)
line = lines[436]

# Find the exact prefix
prefix = '   - **Status:** dokeman PRD **FINAL**; state stabil; rev 34 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 33).'
print("Prefix length:", len(prefix))
print("Line starts with prefix:", line.startswith(prefix))

# Check char-by-char
for i in range(len(prefix)):
    if prefix[i] != line[i]:
        print(f"Mismatch at {i}: prefix={prefix[i]!r} line={line[i]!r}")
        break
else:
    print("Prefix matches exactly")
    print("Remaining content starts with:", repr(line[len(prefix):][:100]))
