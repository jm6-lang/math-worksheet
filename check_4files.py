import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'

# Check the 4 specific curriculum files + movies files mentioned
files_to_check = [
    'curriculum/post_070.md',
    'curriculum/post_071.md',
    'curriculum/post_105.md',
    'curriculum/post_106.md',
    'movies/post_042.md',
]

for rel in files_to_check:
    fp = os.path.join(repo, rel)
    if not os.path.exists(fp):
        print(f'{rel}: NOT FOUND')
        continue
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    
    content = raw.strip()
    # Split frontmatter properly
    if content.startswith('---'):
        end = content.find('\n---', 4)
        if end >= 0:
            frontmatter = content[3:end].strip()
            body = content[end+4:].strip()
        else:
            frontmatter = ''
            body = content
    else:
        frontmatter = ''
        body = content
    
    # Find links
    quark = re.findall(r'pan\.quark\.cn/\S+', body)
    xunlei = re.findall(r'xunlei\.com/\S+', body)
    baidu = re.findall(r'pan\.baidu\.com/\S+', body)
    ali = re.findall(r'alipan\.com/\S+', body)
    
    # Get title
    title_m = re.search(r'^title:\s*(.+?)\s*$', frontmatter, re.MULTILINE)
    title = title_m.group(1).strip().strip('"\'') if title_m else '(no title)'
    
    print(f'{rel}:')
    print(f'  title: {title}')
    print(f'  quark: {quark}')
    print(f'  xunlei: {xunlei}')
    print(f'  baidu: {baidu}')
    print(f'  ali: {ali}')
    print(f'  body length: {len(body)}')
