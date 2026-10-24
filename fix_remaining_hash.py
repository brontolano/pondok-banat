import os
p = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

old = '9d7fe316159efa9c781fa0263187a7e707'
new = 'b1aec91fbc7b97e87f71908b6019f5d335ce8975'
count = content.count(old)
print("Occurrences to replace:", count)
content = content.replace(old, new)
with open(p, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done. Remaining:", content.count(old))
print("New hash present:", new in content)
