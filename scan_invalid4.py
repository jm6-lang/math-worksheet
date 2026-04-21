import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
dirs = ['tools', 'self-media', 'book', 'movies', 'AIknowledge', 'curriculum', 'edu-knowlege', 'chinese-traditional']

invalid_files = []

for d in dirs:
    dpath = os.path.join(repo, d)
    if not os.path.exists(dpath):
        continue
    files = [f for f in os.listdir(dpath) if f.endswith('.md') and f != 'index.md']
    
    for f in files:
        fp = os.path.join(dpath, f)
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                raw = fh.read()
            
            content = raw.strip()
            if not content.startswith('---'):
                continue
            end = content.find('\n---\n', 4)
            if end == -1:
                end = content.find('\n---', 4)
            if end == -1:
                continue
            frontmatter = content[3:end].strip()
            body = content[end+4:].strip()
            
            # Check for ANY valid download links in body
            quark = re.findall(r'pan\.quark\.cn/s/\w+', body)
            xunlei = re.findall(r'xunlei\.com/s/\w+', body)
            baidu = re.findall(r'pan\.baidu\.com/s/\w+', body)
            ali = re.findall(r'alipan\.com/s/\w+', body)
            
            has_link = bool(quark or xunlei or baidu or ali)
            
            # Also check if source field in frontmatter has a valid link
            source_m = re.search(r'^source:\s*(.+?)\s*$', frontmatter, re.MULTILINE)
            source = source_m.group(1).strip().strip('"\'') if source_m else ''
            source_has_link = bool(re.search(r'pan\.(quark|baidu|ali)|xunlei', source, re.I))
            
            if not has_link and not source_has_link:
                title_m = re.search(r'^title:\s*(.+?)\s*$', frontmatter, re.MULTILINE)
                title = title_m.group(1).strip().strip('"\'') if title_m else ''
                invalid_files.append({
                    'rel': f'{d}/{f}',
                    'title': title,
                    'body_len': len(body),
                })
        except Exception as e:
            pass

print(f'Files with NO valid download links anywhere: {len(invalid_files)}')
for item in sorted(invalid_files, key=lambda x: x['rel']):
    print(f"  {item['rel']}: title='{item['title']}' body={item['body_len']}")

print('\nThese files will be deleted.')
