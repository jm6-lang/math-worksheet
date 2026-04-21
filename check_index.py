import os, json

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'

# Read movies and curriculum index pages to see how they list the posts
for idx_file in ['movies/index.md', 'curriculum/index.md']:
    fp = os.path.join(repo, idx_file)
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Find lines containing the post numbers we care about
        lines = content.splitlines()
        print(f'\n=== {idx_file} ===')
        for line in lines:
            for num in ['127', '128', '034', '035', '070', '071', '105', '106']:
                if num in line:
                    print(f'  {line.strip()[:150]}')
                    break
