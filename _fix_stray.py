path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove stray double-asterisk right after 'ulang.' before the Rev 49 entry
old = 'verifikasi ulang.**\n\n26. **Rev. 49'
new = 'verifikasi ulang.\n\n26. **Rev. 49'
if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed stray **')
else:
    print('Pattern not found')
    # show surrounding context
    idx = content.find('ulang.')
    print(repr(content[idx-20:idx+60]))
