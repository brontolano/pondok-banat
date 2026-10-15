#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_prd2.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r') as f:
        content = f.read()

    replacements = [
        (
            "model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema; perlu ditambahkan jika fitur progress kitab akan dibangun.",
            "> **Catatan Prisma:** model `KitabProgress` (Student + Subject) dan `Sertakan` (User) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut."
        ),
        (
            "Catatan: model `KitabProgress` hanya direferensikan, belum didefinisikan.",
            "- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). `KitabProgress` (baris 203) & `Sertakan` (baris 218) didefinisikan."
        ),
    ]

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print("Replaced:", old[:70])
        else:
            print("NOT FOUND:", old[:70])

    with open(path, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    main()
