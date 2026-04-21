import os
from collections import defaultdict

base = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
title_map = defaultdict(list)

for root, dirs, files in os.walk(base):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        if fname in ['_index.md', 'index.md', '目录.md']:
            continue
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, base).replace('\\', '/')
        
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            title = None
            for line in content.split('\n')[:10]:
                ls = line.strip()
                if ls.startswith('title:'):
                    t = ls.split('title:', 1)[1].strip().strip('"').strip("'")
                    title = t
                    break
            
            if title:
                title_map[title].append(rel)
        except Exception as e:
            print('Error:', rel, str(e)[:50])

print('=== Duplicate titles ===')
dups = {t: fs for t, fs in sorted(title_map.items()) if len(fs) > 1}
for title, flist in dups.items():
    safe_title = title.encode('ascii', errors='replace').decode()
    print('[%d] %s' % (len(flist), safe_title[:50]))
    for f in flist:
        print('  ', f)
    print()

print('Total duplicate groups:', len(dups))
print('Total unique titles:', len(title_map))
print('Total files with title:', sum(len(fs) for fs in title_map.values()))
