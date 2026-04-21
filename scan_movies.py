import subprocess, base64
from collections import defaultdict

# Get movies directory contents
r = subprocess.run(
    ['gh', 'api', 'repos/jm6-lang/resource-portal/contents/docs/movies',
     '--jq', '.[] | select(.type=="file") | {name: .name, sha: .sha}'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
try:
    import json
    files = json.loads(r.stdout)
except:
    print('JSON parse error:', r.stdout[:200])
    files = []

print('Movies files:', len(files))
title_map = defaultdict(list)

for f in files:
    fname = f.get('name', '')
    if not fname.endswith('.md'):
        continue
    if fname in ['_index.md', 'index.md']:
        continue
    
    # Get content to extract title
    r2 = subprocess.run(
        ['gh', 'api', 
         'repos/jm6-lang/resource-portal/contents/docs/movies/' + fname,
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
            title_map[title].append('movies/' + fname)
    except Exception as e:
        print('Error', fname, ':', str(e)[:50])

print('\n=== Duplicate titles in movies/ ===')
dups = {t: fs for t, fs in title_map.items() if len(fs) > 1}
for title, flist in sorted(dups.items()):
    print('[%d] %s' % (len(flist), repr(title[:40])))
    for f in flist:
        print('  ', f)
print('Total dups:', len(dups))
print('Total unique titles:', len(title_map))
