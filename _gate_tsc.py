import subprocess
r = subprocess.run(['npx','tsc','--noEmit'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True, timeout=120)
print('tsc exit:', r.returncode)
print('tsc stdout:', r.stdout[-2000:])
print('tsc stderr:', r.stderr[-2000:])
