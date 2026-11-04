import json
import os

# Check .next build manifest
bm_path = '/opt/data/home/workspace/dev/pondok-banat/.next/build-manifest.json'
if os.path.exists(bm_path):
    with open(bm_path) as f:
        data = json.load(f)
    print('BUILD_MANIFEST_KEYS:', list(data.keys())[:8])
    nc = data.get('nextConfig')
    if isinstance(nc, str):
        print('NEXT_CONFIG:', nc[:300])
    else:
        print('NEXT_CONFIG:', nc if nc else 'N/A')

# Check .next packages
pkg_path = '/opt/data/home/workspace/dev/pondok-banat/.next/.buildbundler/ignoredPackages.json'
if os.path.exists(pkg_path):
    with open(pkg_path) as f:
        pkgs = json.load(f)
    print('BUILD_PACKAGES:', type(pkgs), len(pkgs) if isinstance(pkgs, (list, dict)) else 'N/A')

# Check node_modules
nm = '/opt/data/home/workspace/dev/pondok-banat/node_modules'
print('NODE_MODULES_DIRS:', len(os.listdir(nm)) if os.path.isdir(nm) else 'N/A')

# Check versions
for p in ['next', 'react', 'react-dom', 'typescript', 'eslint', 'prisma']:
    fp = os.path.join(nm, p, 'package.json')
    if os.path.exists(fp):
        with open(fp) as f:
            import json
            d = json.load(f)
            print('VERSION_%s: %s' % (p.upper(), d.get('version')))
    else:
        print('VERSION_%s: NOT_FOUND' % p.upper())
