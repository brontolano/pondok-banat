import subprocess
r = subprocess.run(['npx','next','build'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True, timeout=300)
print('next build exit:', r.returncode)
print('next build stdout:', r.stdout[-3000:])
print('next build stderr:', r.stderr[-3000:])
