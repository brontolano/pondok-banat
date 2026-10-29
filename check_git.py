import subprocess

def run(cmd):
    r = subprocess.run(cmd, shell=True, cwd='/opt/data/home/workspace/dev/pondok-banat',
                       capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

# Check git status
stdout, stderr, rc = run('git status --short')
print('Git status:')
print(stdout if stdout else '(clean)')

# Check diff stat of staging area
stdout, stderr, rc = run('git diff --stat')
print('\nUnstaged diff stat:')
print(stdout if stdout else '(no unstaged diff)')

# Check staged diff
stdout, stderr, rc = run('git diff --cached --stat')
print('\nStaged diff stat:')
print(stdout if stdout else '(no staged diff)')
