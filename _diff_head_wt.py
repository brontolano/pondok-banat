import subprocess

ws = "/opt/data/home/workspace/dev/pondok-banat"

# Get the diff
r = subprocess.run(["git", "diff", "HEAD", "--", "PRD-PONDOK-BANAT.md"], capture_output=True, text=True)
diff = r.stdout
print("DIFF LENGTH:", len(diff))
print("=== FIRST 3000 CHARS ===")
print(diff[:3000])
print("\n=== LAST 3000 CHARS ===")
print(diff[-3000:])
