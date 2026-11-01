PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
src = open(PATH, encoding='utf-8').read()

start_anchor = '> **Verifikasi fresh dilakukan:** 1 November 2026'
i = src.find(start_anchor)
print('start idx:', i)

# end anchor = full line 464 tail (unique)
end_anchor = 'State stabil, tidak ada perubahan signifikan dari Rev. 787 (data terkonsisten).'
j = src.find(end_anchor, i)
print('end idx:', j)
if i >= 0 and j >= 0:
    block = src[i:j + len(end_anchor)]
    print('---FULL BLOCK REPR (len=%d)---' % len(block))
    print(repr(block))
    print('---LAST 300 CHARS REPR---')
    print(repr(block[-300:]))
