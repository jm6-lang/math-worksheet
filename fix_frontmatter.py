# -*- coding: utf-8 -*-
import os, glob, re

dir_path = 'docs/curriculum'
fixed = 0

for f in sorted(glob.glob(os.path.join(dir_path, 'post_1[0-3][0-9].md'))):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    lines = content.split('\n')
    new_lines = []
    in_frontmatter = False
    fm_count = 0
    changed = False
    
    for line in lines:
        if line.strip() == '---':
            fm_count += 1
            if fm_count <= 2:
                in_frontmatter = (fm_count == 1)
            new_lines.append(line)
            continue
        
        if in_frontmatter:
            # Replace double-quoted YAML values with single-quoted ones
            # Pattern: key: "value" -> key: 'value'
            # But need to handle internal quotes carefully
            m = re.match(r'^(\s*\w+\s*:\s*)"(.*)"', line)
            if m:
                key_part = m.group(1)
                value = m.group(2)
                # Escape any single quotes in value by doubling them
                value_escaped = value.replace("'", "''")
                # Replace any remaining ASCII double quotes inside value with Chinese angle quotes
                # Actually, just use single quotes for the whole value
                new_line = key_part + "'" + value_escaped + "'"
                if new_line != line:
                    changed = True
                new_lines.append(new_line)
                continue
        
        new_lines.append(line)
    
    if changed:
        new_content = '\n'.join(new_lines)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        fixed += 1
        print(f'Fixed: {os.path.basename(f)}')

print(f'Total fixed: {fixed}')
