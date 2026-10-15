#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_prd.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r') as f:
        lines = f.readlines()

    # Find all "## 13. REVISI TERBARU" occurrences
    indices = []
    for i, line in enumerate(lines):
        if '## 13. REVISI TERBARU (Rev. 53' in line:
            indices.append(i)
    print("Found '## 13. REVISI TERBARU (Rev. 53' at lines:", [i+1 for i in indices])

    if len(indices) < 2:
        print("No duplicate found, exiting.")
        return

    # Remove the first occurrence to just before the second occurrence
    # lines[indices[0]] is the first header; lines[indices[1]] is the second header
    first = indices[0]
    second = indices[1]
    # Remove lines from first to second-1 (inclusive of first, exclusive of second)
    new_lines = lines[:first] + lines[second:]

    with open(path, 'w') as f:
        f.writelines(new_lines)

    print("Removed duplicate section 13. New line count:", len(new_lines))
    print("New '## 13. REVISI TERBARU' count:", sum(1 for l in new_lines if '## 13. REVISI TERBARU (Rev. 53' in l))

if __name__ == '__main__':
    main()
