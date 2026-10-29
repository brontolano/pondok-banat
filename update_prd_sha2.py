path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
sha = 'd307fc43974a82cbd70be401c0b1cfb084c42603'
with open(path, 'r') as f:
    content = f.read()
content = content.replace('9881fb2bb82e4015d5ea42b889d6045f615891f0', sha)
with open(path, 'w') as f:
    f.write(content)
print('Updated SHA to', sha)
