import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
dirs = ['tools', 'self-media', 'book', 'movies', 'AIknowledge', 'curriculum', 'edu-knowlege', 'chinese-traditional']

results = {}

for d in dirs:
    dpath = os.path.join(repo, d)
    if not os.path.exists(dpath):
        continue
    files = [f for f in os.listdir(dpath) if f.endswith('.md') and f != 'index.md']
    
    file_info = {}
    for f in files:
        fp = os.path.join(dpath, f)
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
            # Extract frontmatter title
            m = re.search(r'^---\s*\ntitle:\s*["\']?(.+?)["\']?\s*\n', content, re.MULTILINE)
            # Extract first heading
            m2 = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            # Extract source/quark link
            m3 = re.search(r'(pan\.quark\.cn[^\s\'"\)]+)', content)
            frontmatter_title = m.group(1).strip() if m else ''
            heading_title = m2.group(1).strip() if m2 else ''
            quark_link = m3.group(1).strip() if m3 else ''
            
            body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL | re.MULTILINE).strip()
            
            file_info[f] = {
                'frontmatter_title': frontmatter_title,
                'heading_title': heading_title,
                'quark_link': quark_link,
                'has_body': len(body) > 10,
                'body_preview': body[:50]
            }
        except Exception as e:
            file_info[f] = {'error': str(e)}

    # Find groups with same frontmatter title
    by_title = {}
    for fn, info in file_info.items():
        t = info.get('frontmatter_title', fn)
        if t not in by_title:
            by_title[t] = []
        by_title[t].append(fn)
    
    dups = {t: fl for t, fl in by_title.items() if len(fl) > 1}
    empty_body = [fn for fn, info in file_info.items() if not info.get('has_body', False)]
    
    results[d] = {
        'total': len(files),
        'dups': dups,
        'empty_body_count': len(empty_body),
        'empty_body_files': empty_body[:5],
        'file_info': file_info
    }
    
    print(f'{d}: {len(files)} files, {len(dups)} title-dup groups, {len(empty_body)} empty-body files')

# Write full report
import json
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\dup_report.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('\nReport written to dup_report.json')
