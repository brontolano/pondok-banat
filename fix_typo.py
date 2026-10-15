import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the typo: data-pondokanat -> data-pondappanat
content = content.replace('data-pondokanat', 'data-pondappanat')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. Checking remaining typos:")
import subprocess
result = subprocess.run(['grep', '-n', 'pondakanat', path], capture_output=True, text=True)
print("grep 'pondakanat':", result.stdout if result.stdout else "(none found, good)")
result2 = subprocess.run(['grep', '-n', 'pondappanat', path], capture_output=True, text=True)
print("grep 'pondappanat':", result2.stdout if result2.stdout else "(none found)")
