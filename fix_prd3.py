#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_prd3.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r') as f:
        content = f.read()

    # Line 330: "- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). `KitabProgress` (baris 203) & `Sertakan` (baris 218) didefinisikan."

    # The duplicated segment is: " `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). `KitabProgress` (baris 203) & `Sertakan` (baris 218) didefinisikan."
    # Remove it.

    dup = " `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22). `KitabProgress` (baris 203) & `Sertakan` (baris 218) didefinisikan."
    if dup in content:
        content = content.replace(dup, "", 1)
        print("Fixed 330")
    else:
        print("Pattern not found")
        # Show context around the first 'driver client' occurrence after index 0
        idx = content.find('driver client', 10)
        if idx >= 0:
            print("Context:", repr(content[idx-30:idx+200]))

    with open(path, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    main()
