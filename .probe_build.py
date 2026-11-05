import subprocess, sys

def run(cmd, timeout=180):
    print('$', ' '.join(cmd))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        print('EXIT:', r.returncode)
        out = (r.stdout or '').strip()
        err = (r.stderr or '').strip()
        if out:
            print('OUT:', out[-1500:])
        if err:
            print('ERR:', err[-800:])
        return r.returncode
    except subprocess.TimeoutExpired:
        print('TIMEOUT')
        return 124

rc1 = run(['node_modules/.bin/tsc', '--noEmit'], timeout=120)
print('---')
rc2 = run(['node_modules/.bin/eslint', '.'], timeout=120)
print('---')
sys.exit(0)
