import re

with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Fix all occurrences of the old git SHA with the new one
old_sha = 'e91c3b3d302bc4f58f816e20e25ff457451bf9ec'
new_sha = '725c689ac2b3c473cd3e0702f4944918f30ddc52'
count = content.count(old_sha)
content = content.replace(old_sha, new_sha)
print(f'Replaced {count} occurrences of old SHA')

# Fix the header's local branch count
content = content.replace(
    'Local branch **3 commit ahead**, **0 commit behind** origin.main.',
    'Local branch **4 commit ahead**, **0 commit behind** origin.main.'
)

with open('PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print('e91c3b3 count:', content.count('e91c3b3'))
print('725c689 count:', content.count('725c689'))
print('Local branch 3 count:', content.count('Local branch **3 commit ahead**'))
print('Local branch 4 count:', content.count('Local branch **4 commit ahead**'))
