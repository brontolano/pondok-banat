#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_prd4.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r') as f:
        content = f.read()

    # Fix the stale KitabProgress note at line 393 (section 9.1, Catatan Struktur)
    old = "Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema."
    new = "Model `KitabProgress` (Student + Subject, baris 203) & `Sertakan` (User, baris 218) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut."
    if old in content:
        content = content.replace(old, new, 1)
        print("Fixed 393")
    else:
        print("Pattern not found at 393")

    with open(path, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    main()
