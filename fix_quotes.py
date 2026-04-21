import os, glob

dir_path = 'docs/curriculum'
fixed = 0

for f in sorted(glob.glob(os.path.join(dir_path, 'post_1[0-3][0-9].md'))):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    if '\u201c' not in content and '\u201d' not in content:
        continue
    
    new_content = content.replace('\u201c', '\u2018').replace('\u201d', '\u2019')
    
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    fixed += 1
    print(f'Fixed: {os.path.basename(f)}')

print(f'Total fixed: {fixed}')
