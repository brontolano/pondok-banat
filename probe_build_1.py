import subprocess, sys
r = subprocess.run(['npx', 'tsc', '--noEmit'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True, timeout=300)
print('=== TSC ===')
print('exit:', r.returncode)
print(r.stdout[-3000:])
print(r.stderr[-3000:])
