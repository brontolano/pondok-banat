BASE = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(BASE, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
print('TOTAL_LINES', len(lines))

# line 4 (index 3): the header
l4 = lines[3]
print('L4 START:', repr(l4[:80]))
print('L4 END:', repr(l4[-80:]))
print('L4 contains "diblokir Tir" (with h):', 'diblokir Tirith' in l4)
print('L4 contains "diblokir Tir" (no h) at end:', l4.endswith('diblokir Tir'))
print('L4 contains "diblokir Tirith":', 'diblokir Tirith' in l4)
print('L4 ENDSWITH "diblokir Tir\\n":', l4.endswith('\ndiblokir Tir'))

# Find the Rev.57 body section: it starts after "## 17. REVISI TERBARU (Rev. 57"
idx57 = content.find('## 17. REVISI TERBARU (Rev. 57')
print('---Rev.57 body---')
print('Rev57 body starts at char', idx57)
# find the end of Rev.57 line
end57 = content.find('\n', idx57)
print('Rev57 body line len', end57 - idx57)
print(repr(content[idx57:idx57+80]))
print('---end of Rev57 line---')
print(repr(content[end57-60:end57+40]))
