import os

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'

# Check the raw bytes of the index pages for the specific lines
files_to_check = [
    ('movies/index.md', ['post_127', 'post_128']),
    ('curriculum/index.md', ['post_034', 'post_035', 'post_070', 'post_071', 'post_105', 'post_106']),
]

for idx_file, targets in files_to_check:
    fp = os.path.join(repo, idx_file)
    if not os.path.exists(fp):
        continue
    
    with open(fp, 'rb') as f:
        raw = f.read()
    
    text = raw.decode('utf-8', errors='replace')
    
    print(f'\n=== {idx_file} ===')
    for line in text.splitlines():
        for t in targets:
            if t in line:
                # Try to find the actual text between | and | around the post link
                parts = line.split('|')
                for i, p in enumerate(parts):
                    if t in p:
                        left = parts[i-1].strip() if i > 0 else ''
                        right = parts[i+1].strip() if i+1 < len(parts) else ''
                        print(f'  Col left: {repr(left)} -> {repr(left.encode("utf-8").decode("gbk", errors="replace"))}')
                        break
