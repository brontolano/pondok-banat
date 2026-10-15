import subprocess, time
start = time.time()
r = subprocess.run(['./node_modules/.bin/next', 'build'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True, timeout=600)
print('STDOUT (last 3000):', r.stdout[-3000:])
print('STDERR (last 2000):', r.stderr[-2000:])
print('EXIT:', r.returncode)
print('TIME:', round(time.time() - start, 1), 's')
