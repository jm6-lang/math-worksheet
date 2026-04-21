import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
files = [
    ('curriculum', 'post_070.md'),
    ('curriculum', 'post_071.md'),
    ('curriculum', 'post_105.md'),
    ('curriculum', 'post_106.md'),
]

for d, f in files:
    fp = os.path.join(repo, d, f)
    if not os.path.exists(fp):
        print(f'{d}/{f}: NOT FOUND')
        continue
    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    
    # Extract title
    title_m = re.search(r'^---\s*\ntitle:\s*["\']?(.+?)["\']?\s*\n', content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else '(no title)'
    
    # Extract all links
    quark = re.findall(r'pan\.quark\.cn/[^\s<>"\']+', content)
    xunlei = re.findall(r'xunlei[^\s<>"\']+', content)
    
    body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL | re.MULTILINE).strip()
    
    print(f'\n=== {d}/{f} ===')
    print(f'  title: {title}')
    print(f'  quark links: {quark}')
    print(f'  xunlei links: {xunlei}')
    print(f'  body preview: {body[:100]}')
