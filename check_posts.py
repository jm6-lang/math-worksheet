#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import base64
import sys
import os

# Set output encoding
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Check first few post files in each directory for encoding issues
dirs_to_check = [
    ('book', ['post_001.md', 'post_002.md', 'post_003.md']),
    ('tools', ['post_001.md', 'post_002.md', 'post_003.md']),
    ('curriculum', ['post_001.md', 'post_002.md', 'post_003.md']),
    ('movies', ['post_001.md', 'post_002.md', 'post_003.md']),
    ('book/book', ['book_001.md', 'book_002.md', 'book_003.md']),
    ('book/culture', ['culture_001.md', 'culture_002.md', 'culture_003.md']),
    ('book/tcm', ['tcm_001.md', 'tcm_002.md', 'tcm_003.md']),
]

for dir_path, files in dirs_to_check:
    print(f'\n=== {dir_path} ===')
    for filename in files:
        try:
            result = subprocess.run(
                ['gh', 'api', f'repos/jm6-lang/resource-portal/contents/docs/{dir_path}/{filename}', '--jq', '.content'],
                capture_output=True, text=True, timeout=10
            )
            content_b64 = result.stdout.strip()
            if not content_b64:
                print(f'{filename}: NOT FOUND')
                continue
            
            content_bytes = base64.b64decode(content_b64)
            try:
                text = content_bytes.decode('utf-8')
                # Check for replacement chars
                if '\ufffd' in text:
                    print(f'{filename}: HAS U+FFFD REPLACEMENT CHAR')
                else:
                    # Try to find title in frontmatter or first heading
                    lines = text.split('\n')
                    title = 'NOT FOUND'
                    for i, line in enumerate(lines):
                        if line.startswith('title:'):
                            title = line[6:].strip()
                            break
                        if line.startswith('# '):
                            title = line[2:].strip()
                            break
                    # Check first 80 chars
                    preview = lines[0][:80] if lines else ''
                    print(f'{filename}: OK - {repr(preview[:40])}')
            except UnicodeDecodeError as e:
                print(f'{filename}: UTF-8 DECODE ERROR - {e}')
        except Exception as e:
            print(f'{filename}: ERROR - {e}')