import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
dirs = ['tools', 'self-media', 'book', 'movies', 'AIknowledge', 'curriculum', 'edu-knowlege', 'chinese-traditional']

all_dups = []

for d in dirs:
    dpath = os.path.join(repo, d)
    if not os.path.exists(dpath):
        continue
    files = [f for f in os.listdir(dpath) if f.endswith('.md') and f != 'index.md']
    
    titles = {}
    for f in files:
        fp = os.path.join(dpath, f)
        title = f
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
                # Try frontmatter title
                m = re.search(r'^---\s*\ntitle:\s*[\x22\x27]?(.+?)[\x22\x27]?\s*\n', content, re.MULTILINE)
                if not m:
                    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = m.group(1).strip() if m else f.replace('.md', '')
        except:
            title = f

        # Normalize: strip trailing #1 #2 etc
        norm = re.sub(r'\s*#\d+$', '', title.strip())
        if norm not in titles:
            titles[norm] = []
        titles[norm].append((f, title.strip(), fp))

    dups = {k: v for k, v in titles.items() if len(v) > 1}
    if dups:
        print(f'\n=== {d} ({len(files)} files, {len(dups)} dup groups) ===')
        for k, v in sorted(dups.items(), key=lambda x: -len(x[1])):
            print(f'  [{len(v)} files] {k}')
            for fn, t, fp in v:
                print(f'    {fn}: {t[:80]}')
            all_dups.append((d, k, v))
