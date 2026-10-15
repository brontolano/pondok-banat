#!/usr/bin/env python3
import os

root = '/opt/data/home/workspace/dev/pondok-banat'

print("=== Beranda.tsx ===")
with open(os.path.join(root, 'src', 'components', 'Beranda.tsx'), 'r') as f:
    print(f.read())

print("\n\n=== db_summary.py ===")
with open(os.path.join(root, 'db_summary.py'), 'r') as f:
    print(f.read())

print("\n\n=== db_summary.py content ===")
