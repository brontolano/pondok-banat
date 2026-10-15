with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()
idx = content.find('Rev. 51 — 15 Oktober')
if idx > 0:
    chunk = content[idx:idx+3000]
    for line in chunk.split('\n'):
        if 'uidNfc' in line or 'Rev. 51' in line:
            print(repr(line))
