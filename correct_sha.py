path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
sha_prev = '9881fb2bb82e4015d5ea42b889d6045f615891f0'
sha_cur = 'd307fc43974a82cbd70be401c0b1cfb084c42603'
with open(path, 'r') as f:
    content = f.read()
# The PRD file should reference the PREVIOUS commit (9881fb2), not the current commit (d307fc4)
content = content.replace(sha_cur, sha_prev)
with open(path, 'w') as f:
    f.write(content)
print('Updated PRD file to reference PREVIOUS commit', sha_prev)
