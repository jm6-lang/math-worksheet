#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import base64
import sys
import os

# Set output encoding to utf-8
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

dirs = ['book', 'book/book', 'book/culture', 'book/tcm', 'movies', 'self-media', 
        'curriculum', 'edu-knowlege', 'tools', 'chinese-traditional', 'music']

for d in dirs:
    result = subprocess.run(
        ['gh', 'api', f'repos/jm6-lang/resource-portal/contents/docs/{d}', '--jq', '.[] | select(.type == "file") | .name'],
        capture_output=True, text=True
    )
    names = result.stdout.strip()
    count = len([n for n in names.split('\n') if n.strip()])
    print(f'{d}: {count} files')

print('\n--- Checking index.md files for encoding issues ---')

# Now let's check what's in these index files by downloading and checking them
for d in dirs:
    try:
        result = subprocess.run(
            ['gh', 'api', f'repos/jm6-lang/resource-portal/contents/docs/{d}/index.md', '--jq', '.content'],
            capture_output=True, text=True
        )
        content_b64 = result.stdout.strip()
        if not content_b64:
            print(f'{d}/index.md: NOT FOUND')
            continue
        content_bytes = base64.b64decode(content_b64)
        
        # Try to decode
        try:
            text = content_bytes.decode('utf-8')
            # Check for replacement chars
            if '\ufffd' in text or '\u0000' in text:
                print(f'{d}/index.md: HAS REPLACEMENT CHARS (UTF-8 decode had issues)')
            else:
                lines = text.split('\n')
                first_line = lines[0] if lines else ''
                # Clean first line for print
                clean_line = ''.join(c for c in first_line if ord(c) < 0x10000)
                print(f'{d}/index.md: OK - {clean_line[:60]}')
        except Exception as e:
            print(f'{d}/index.md: DECODE ERROR - {e}')
    except Exception as e:
        print(f'{d}/index.md: ERROR - {e}')