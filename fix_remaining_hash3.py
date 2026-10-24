import os
p = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

old = '9d7fe31'
new = 'b1aec91fbc7b97e87f71908b6019f5d335ce8975'
count = content.count(old)
print("Occurrences of '9d7fe31' to replace:", count)
content = content.replace(old, new)
with open(p, 'w', encoding='utf-8') as f:
    f.write(content)
print("Remaining '9d7fe31':", content.count('9d7fe31'))
print("New hash count:", content.count(new))
