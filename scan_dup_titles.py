import subprocess, base64
from collections import defaultdict

dirs = ['movies', 'book', 'healthy', 'music', 'tools']
title_map = defaultdict(list)

for d in dirs:
    r = subprocess.run(
        ['gh', 'api', 'repos/jm6-lang/resource-portal/contents/docs/' + d,
         '--jq', '.[] | select(.type=="file") | .name'],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    files = [f for f in r.stdout.strip().split('\n') if f and f.endswith('.md')]
    print(d, ':', len(files), 'files')

    for fname in files:
        if fname in ['_index.md', 'index.md']:
            continue
        r2 = subprocess.run(
            ['gh', 'api',
             'repos/jm6-lang/resource-portal/contents/docs/' + d + '/' + fname,
             '--jq', '.content'],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        try:
            content = base64.b64decode(r2.stdout.strip()).decode('utf-8', errors='replace')
            title = None
            for line in content.split('\n')[:5]:
                ls = line.strip()
                if ls.startswith('title:'):
                    t = ls.split('title:', 1)[1].strip().strip('"').strip("'")
                    title = t
                    break
            if title:
                title_map[title].append(d + '/' + fname)
        except Exception as e:
            pass

print('\n=== Duplicate titles ===')
for title, files in sorted(title_map.items()):
    if len(files) > 1:
        print('[%d] %s' % (len(files), title[:50].encode('ascii', errors='replace').decode()))
        for f in files:
            print('  -', f)
        print()
