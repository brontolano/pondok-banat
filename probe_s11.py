PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
src = open(PATH, encoding='utf-8').read()
i = src.find('> **Verifikasi fresh dilakukan:** 1 November 2026')
print('start idx:', i)
if i >= 0:
    j = src.find('data terkonsisten).', i)
    print('end idx:', j)
    if j >= 0:
        block = src[i:j + len('data terkonsisten).')]
        print('---BLOCK REPREPR---')
        print(repr(block))
