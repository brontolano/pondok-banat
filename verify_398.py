#!/usr/bin/env python3
content = open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md').read()
checks = [
    ('§11 title updated to Rev. 116–398', 'Rev. 116–398 — 28 Oktober 2026 WIB' in content),
    ('§11 title has Rev. 116–398', '## 11. REVISI TERBARU (Rev. 116–398' in content),
    ('Compact changelog has Rev. 398 entry', '    398. 21 Oktober 2026 (WIB):' in content),
    ('§12 Rev. 398 section added', '## 12. REVISI TERBARU (Rev. 398 — 21 Oktober 2026 WIB)' in content),
    ('Git HEAD ref updated to 7b169af', '7b169afb0d544dc9bbbeaeea17e90333400445ff' in content),
    ('M02a (NFC) status included', 'M02a (NFC)' in content),
    ('Auth hardcode noted', 'Login.tsx' in content),
    ('Beranda hardcode noted', 'Beranda.tsx' in content),
    ('Build quality gate noted', 'NOT RE-RUNABLE' in content),
]
for name, result in checks:
    print(('✓' if result else '✗'), name)
print()
print('All checks passed:', all(r for _, r in checks))
