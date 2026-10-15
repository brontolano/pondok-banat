import subprocess
import sys

def run(cmd):
    print('Running:', ' '.join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True, cwd='/opt/data/home/workspace/dev/pondok-banat')
    print('STDOUT:', r.stdout[-2000:] if r.stdout else '(empty)')
    print('STDERR:', r.stderr[-2000:] if r.stderr else '(empty)')
    print('EXIT:', r.returncode)
    return r.returncode

rc1 = run(['npx', 'tsc', '--noEmit'])
rc2 = run(['npm', 'run', 'lint'])
rc3 = run(['npm', 'run', 'build'])
print('=== SUMMARY ===')
print('tsc:', rc1, 'lint:', rc2, 'build:', rc3)
