import re

with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Count occurrences of key patterns
print('Rev. 268 count:', content.count('Rev. 268'))
print('Rev. 269 count:', content.count('Rev. 269'))
print('18 commit count:', content.count('18 commit'))
print('5cf80a0 count:', content.count('5cf80a0c810c517d11b6ebc0aa909ab10864abae'))
print('342ede6 count:', content.count('342ede6926c0064539bf43eba8dc6639b895c827'))
print('Total lines:', content.count(chr(10)) + 1)
