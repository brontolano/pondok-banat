with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()
lines = content.split('\n')
print("Total lines:", len(lines))
print("Line 4 length:", len(lines[3]))
print("Line 4 full:", repr(lines[3]))
