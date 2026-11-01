import subprocess
r = subprocess.run(['npx', 'next', 'build'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True, timeout=600)
print('=== NEXT BUILD ===')
print('exit:', r.returncode)
out = (r.stdout or '') + (r.stderr or '')
print(out[-5000:])
