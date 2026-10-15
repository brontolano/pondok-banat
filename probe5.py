import os
import re
from collections import Counter

dir_path = '.data-pondokbanat/Pdf had mata pelajaran'
files = os.listdir(dir_path)
print('Total files:', len(files))

# Extract subject from filename
pattern = re.compile(r'RPP PELAJARAN (\S+) KELAS (\d+)(?: \((.+)\))?\.pdf')
# Also handle SILABUS
silabus_pattern = re.compile(r'SILABUS (.+)\.pdf')

subject_count = Counter()
class_count = Counter()
for f in files:
    m = pattern.match(f)
    if m:
        subject = m.group(1).strip()
        cls = m.group(2)
        subject_count[subject] += 1
        class_count[cls] += 1
    else:
        m2 = silabus_pattern.match(f)
        if m2:
            subject = m2.group(1).strip()
            subject_count['SILABUS:' + subject] += 1
            print('SILABUS:', f)

print()
print('=== Subject counts (from RPP filenames):')
for s, c in sorted(subject_count.items()):
    print(f'  {s}: {c}')
print('Total distinct subjects:', len(subject_count))
print()
print('=== Total RPP files:', sum(c for s, c in subject_count.items() if not s.startswith('SILABUS')))
print('Total SILABUS files:', sum(c for s, c in subject_count.items() if s.startswith('SILABUS')))
print()
print('=== Class distribution:')
for c, n in sorted(class_count.items()):
    print(f'  Kelas {c}: {n}')
