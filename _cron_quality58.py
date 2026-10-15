import subprocess
import sys

def run(cmd, label):
    print("=" * 60)
    print("RUNNING: %s" % label)
    print("CMD: %s" % " ".join(cmd))
    print("-" * 60)
    result = subprocess.run(cmd, cwd='/opt/data/home/workspace/dev/pondok-banat',
                            capture_output=True, text=True, timeout=300)
    print("EXIT CODE: %d" % result.returncode)
    if result.stdout:
        print("STDOUT (last 2000 chars):")
        print(result.stdout[-2000:])
    if result.stderr:
        print("STDERR (last 2000 chars):")
        print(result.stderr[-2000:])
    print("=" * 60)
    return result.returncode

rc1 = run(['npx', 'tsc', '--noEmit'], 'TypeScript type-check')
rc2 = run(['npm', 'run', 'lint'], 'ESLint')
rc3 = run(['npm', 'run', 'build'], 'Next.js build')

print("\n\nSUMMARY:")
print("tsc --noEmit: %s" % rc1)
print("npm run lint: %s" % rc2)
print("npm run build: %s" % rc3)
