import os
nd = 0
nf = 0
for r, d, s in os.walk('node_modules'):
    nd += len(d)
    nf += len(s)
print('node_modules dirs:', nd, 'files:', nf)
