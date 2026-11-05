import subprocess, sys

try:
    r = subprocess.run(['node_modules/.bin/next', 'build'], capture_output=True, text=True, timeout=180)
    print('EXIT:', r.returncode)
    out = (r.stdout or '').strip()
    err = (r.stderr or '').strip()
    if out:
        print('OUT:', out[-1500:])
    if err:
        print('ERR:', err[-800:])
except subprocess.TimeoutExpired:
    print('TIMEOUT (180s)')
