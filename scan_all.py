import subprocess, base64, json
from collections import defaultdict

# Fast: get all movies files titles via git tree content
# Use a single API call to get all file contents from the tree
r = subprocess.run(
    ['gh', 'api', 'repos/jm6-lang/resource-portal/git/trees/main?recursive=1',
     '--jq', '.tree[].path'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
paths = [p for p in r.stdout.strip().split('\n') if p.startswith('docs/movies/post_') and p.endswith('.md')]
print('Movies post files:', len(paths))

# For speed, only check files 129-144 which we know are the Quark ones
# and files from 001-128 to find other duplicates
title_map = defaultdict(list)

for p in paths:
    fname = p.split('/')[-1]
    # Get content
    r2 = subprocess.run(
        ['gh', 'api', 'repos/jm6-lang/resource-portal/contents/' + p,
         '--jq', '.content'],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    try:
        raw = r2.stdout.strip()
        content = base64.b64decode(raw).decode('utf-8', errors='replace')
        title = None
        for line in content.split('\n')[:8]:
            ls = line.strip()
            if ls.startswith('title:'):
                t = ls.split('title:', 1)[1].strip().strip('"').strip("'")
                title = t
                break
        if title:
            title_map[title].append(p)
    except Exception as e:
        pass

print('\n=== Duplicate titles ===')
dups = {t: fs for t, fs in sorted(title_map.items()) if len(fs) > 1}
for title, flist in dups.items():
    print('[%d] %s' % (len(flist), repr(title[:50])))
    for f in flist:
        print('  -', f)
print('\nTotal duplicate groups:', len(dups))
print('Total unique titles:', len(title_map))
