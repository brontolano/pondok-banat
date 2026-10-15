with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

line = lines[436]

prefix = '   - **Status:** dokeman PRD **FINAL**; state stabil; rev 34 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 33).'

print("Prefix:", repr(prefix))
print("Line:", repr(line))
print()
print("Prefix[15:25]:", repr(prefix[15:25]))
print("Line[15:25]:", repr(line[15:25]))
