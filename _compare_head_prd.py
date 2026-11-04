import subprocess

ws = "/opt/data/home/workspace/dev/pondok-banat"
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout

# Head version line 3
head = run(["git", "show", "HEAD:PRD-PONDOK-BANAT.md"])
head_lines = head.splitlines()
print("HEAD line 1:", head_lines[0])
print("HEAD line 2:", head_lines[1] if len(head_lines) > 1 else "(none)")
print("HEAD line 3:", head_lines[2] if len(head_lines) > 2 else "(none)")
print("HEAD total lines:", len(head_lines))

# Working tree line 3
with open(ws + "/PRD-PONDOK-BANAT.md") as f:
    wt_lines = f.readlines()
print("\nWT line 1:", wt_lines[0].rstrip())
print("WT line 2:", wt_lines[1].rstrip())
print("WT line 3:", wt_lines[2].rstrip())
print("WT total lines:", len(wt_lines))

# Compare first 5 lines
print("\n=== FIRST 5 LINES DIFF ===")
for i in range(5):
    h = head_lines[i].rstrip() if i < len(head_lines) else "(missing)"
    w = wt_lines[i].rstrip() if i < len(wt_lines) else "(missing)"
    if h != w:
        print(f"line {i+1}: HEAD | {h[:120]}")
        print(f"line {i+1}: WT  | {w[:120]}")

# Also check the tail of HEAD vs working tree
print("\n=== TAIL ===")
print("HEAD last line:", head_lines[-1].rstrip() if head_lines else "(empty)")
print("WT last line:", wt_lines[-1].rstrip())
