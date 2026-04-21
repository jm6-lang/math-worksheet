import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
# Check a few suspicious ones
files_to_check = [
    'tools/post_225.md',
    'book/post_001.md',
    'movies/post_005.md',
    'movies/post_042.md',  # was mentioned in prev scan
    'curriculum/post_070.md',
    'curriculum/post_071.md',
    'curriculum/post_105.md',
    'curriculum/post_106.md',
]

for rel in files_to_check:
    fp = os.path.join(repo, rel)
    if not os.path.exists(fp):
        print(f'{rel}: NOT FOUND')
        continue
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL | re.MULTILINE).strip()
    
    # Find ALL link-like strings
    all_links = re.findall(r'https?://[^\s<>"\']+', body)
    
    title_m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*\n', content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else ''
    
    print(f'\n{rel}:')
    print(f'  title: {title}')
    print(f'  links: {all_links[:5]}')
    print(f'  body[:200]: {body[:200]}')
