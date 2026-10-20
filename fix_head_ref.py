#!/usr/bin/env python3
# Fix git rev-parse HEAD = reference in header of PRD-PONDOK-BANAT.md
path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "`git rev-parse HEAD` = `3bd1a603234083be69ee575971949538e94cc042`"
new = "`git rev-parse HEAD` = `8a5e6bd6b7be34a70687241019d31b7148c31811`"

count = content.count(old)
print(f"Found {count} occurrences of old HEAD ref")
content = content.replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
