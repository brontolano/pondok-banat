with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r', encoding='utf-8') as f:
    content = f.read()
# Find the Rev. 19 banner
idx = content.find('Rev. 19')
print('Rev. 19 at index:', idx)
# Show the region around "Perbaikan"
p1 = content.find('Perbaikan')
print('Perbaikan at index:', p1)
print('Context around Perbaikan:')
print(repr(content[p1-50:p1+100]))
# Check if the pattern would match
import re
pattern = r'> \*\*Rev\. 19.*?\*\*Perbaikan:.*?Rev\. 18 = dokumen PRD sebelumnya\.'
match = re.search(pattern, content, flags=re.DOTALL)
print('Pattern match:', match is not None)
if not match:
    # Try to find what's different
    # Check for the exact text
    print('Has "**Perbaikan:**":', '**Perbaikan:**' in content)
    print('Has "Perbaikan:":', 'Perbaikan:' in content)
    print('Has "Rev. 18 = dokumen PRD sebelumnya.":', 'Rev. 18 = dokumen PRD sebelumnya.' in content)
