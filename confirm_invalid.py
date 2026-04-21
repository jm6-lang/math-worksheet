import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'

# True invalid files (no valid download links)
true_invalid = [
    'tools/post_225.md',
    'book/post_001.md',
    'movies/post_042.md',
    'movies/post_005.md',
    'movies/post_009.md',
    'movies/post_046.md',
]

print('Checking true invalid files:')
for rel in true_invalid:
    fp = os.path.join(repo, rel)
    if not os.path.exists(fp):
        print(f'{rel}: NOT FOUND')
        continue
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    
    content = raw.strip()
    body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL | re.MULTILINE).strip()
    
    # Find any http/https links
    http_links = re.findall(r'https?://[^\s<>"\']+', body)
    
    title_m = re.search(r'^---\s*\ntitle:\s*["\']?(.+?)["\']?\s*\n', content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else '(no title)'
    
    print(f'\n{rel}:')
    print(f'  title: {title}')
    print(f'  http links: {http_links}')
    print(f'  body[:150]: {body[:150]}')
