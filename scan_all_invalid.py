import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
dirs = ['tools', 'self-media', 'book', 'movies', 'AIknowledge', 'curriculum', 'edu-knowlege', 'chinese-traditional']

# Comprehensive scan - find ALL files with no valid download links
all_files = []
invalid_files = []

for d in dirs:
    dpath = os.path.join(repo, d)
    if not os.path.exists(dpath):
        continue
    files = [f for f in os.listdir(dpath) if f.endswith('.md') and f != 'index.md']
    
    for f in files:
        fp = os.path.join(dpath, f)
        rel = f'{d}/{f}'
        try:
            with open(fp, 'rb') as fh:
                raw_bytes = fh.read()
            
            # Try UTF-8 first
            try:
                content = raw_bytes.decode('utf-8')
            except:
                content = raw_bytes.decode('gbk', errors='ignore')
            
            content = content.strip()
            if not content.startswith('---'):
                all_files.append({'rel': rel, 'reason': 'no frontmatter', 'is_valid': False})
                invalid_files.append(rel)
                continue
            
            end = content.find('\n---', 4)
            if end == -1:
                all_files.append({'rel': rel, 'reason': 'no frontmatter end', 'is_valid': False})
                invalid_files.append(rel)
                continue
            
            frontmatter = content[3:end].strip()
            body = content[end+4:].strip()
            
            # Check for ANY valid download link
            links = re.findall(r'pan\.(quark\.cn|baidu\.com)|xunlei\.com|alipan\.com', body, re.I)
            has_link = bool(links)
            
            # Also check frontmatter source field
            src_m = re.search(r'^source:\s*(.+?)\s*$', frontmatter, re.MULTILINE)
            src = src_m.group(1).strip().strip('"\'') if src_m else ''
            src_has_link = bool(re.search(r'pan\.|xunlei', src, re.I))
            
            if not has_link and not src_has_link:
                all_files.append({'rel': rel, 'reason': 'no links', 'body_len': len(body)})
                invalid_files.append(rel)
            else:
                all_files.append({'rel': rel, 'reason': 'has links', 'is_valid': True})
        except Exception as e:
            all_files.append({'rel': rel, 'reason': str(e), 'is_valid': False})
            invalid_files.append(rel)

print(f'Total files scanned: {len(all_files)}')
print(f'Invalid (no download links): {len(invalid_files)}')
print()

# Special cases to check
special = ['chinese-traditional/ziwei.md', 'tools/post_225.md']
for rel in invalid_files:
    if any(s in rel for s in special):
        print(f'  *** {rel}')

print()
for item in sorted(invalid_files, key=lambda x: x):
    if not any(s in item for s in special):
        print(f'  {item}')
