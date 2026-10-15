#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python show_line.py <path> <lineno>")
        sys.exit(1)
    path = sys.argv[1]
    lineno = int(sys.argv[2])
    with open(path, 'r') as f:
        lines = f.readlines()
    print("Line", lineno, "repr:")
    print(repr(lines[lineno - 1]))

if __name__ == '__main__':
    main()
