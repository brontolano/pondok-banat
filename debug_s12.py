import io
lines = io.open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', encoding='utf-8').read().splitlines(keepends=True)
print('total lines:', len(lines))
for sub in ['## 11. REVISI TERBARU','## 12. REVISI TERBARU (Rev. 380','## 13. DAFTAR REVISI']:
    for i,l in enumerate(lines):
        if sub in l:
            print(sub, '->', i+1)
            break
print('line 4:', repr(lines[3][:80]))
print('line 412:', repr(lines[412][:80]))
print('line 1232:', repr(lines[1232][:80]))
print('line 1233:', repr(lines[1233][:80]))
