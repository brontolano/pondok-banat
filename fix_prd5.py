#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_prd5.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r') as f:
        lines = f.readlines()

    # Fix line 393 specifically (index 392)
    # Old text at line 393: "Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema."
    # New text: "Model `KitabProgress` (Student + Subject, baris 203) & `Sertakan` (User, baris 218) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut."

    old = "Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema."
    new = "Model `KitabProgress` (Student + Subject, baris 203) & `Sertakan` (User, baris 218) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut."

    if old in lines[392]:
        lines[392] = lines[392].replace(old, new, 1)
        print("Fixed line 393")
    else:
        print("Pattern not found in line 393")
        print("Context:", repr(lines[392][:200]))

    with open(path, 'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
    main()
