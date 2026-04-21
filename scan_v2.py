import os, re

base = r'C:\Users\Administrator\Desktop\新建文件夹\zibll'
findings = []

# Focus on HIGH RISK patterns
patterns = {
    'eval(': r'\beval\s*\(',
    'base64_decode': r'base64_decode\s*\(',
    'gzinflate': r'gzinflate\s*\(',
    'gzuncompress': r'gzuncompress\s*\(',
    'str_rot13': r'str_rot13\s*\(',
    'create_function': r'create_function\s*\(',
    'shell_exec': r'\bshell_exec\s*\(',
    'system(': r'\bsystem\s*\(',
    'passthru': r'\bpassthru\s*\(',
    'popen': r'\bpopen\s*\(',
    'proc_open': r'\bproc_open\s*\(',
    'assert(': r'\bassert\s*\(',
    'file_put_contents': r'file_put_contents\s*\(',
    'curl_exec': r'curl_exec\s*\(',
    'fsockopen': r'\bfsockopen\s*\(',
    'DOLLAR_POST': r'\x24_(POST|GET|REQUEST|COOKIE)\s*\[',
    'chmod': r'\bchmod\s*\(',
    'unlink': r'\bunlink\s*\(',
}

for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.php'):
            continue
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, base)
        try:
            with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
        except:
            continue
        for name, pat in patterns.items():
            matches = re.findall(pat, content, re.IGNORECASE)
            if matches:
                findings.append((rel, name, len(matches)))

findings.sort(key=lambda x: -x[2])
for rel, name, count in findings:
    print(f'{count:4d}x  {name:30s}  {rel}')

# Now check the "去授权" file
print('\n\n=== 去授权文件/index.php ===')
try:
    with open(r'C:\Users\Administrator\Desktop\新建文件夹\去授权文件\index.php', 'r', encoding='utf-8', errors='replace') as f:
        print(f.read()[:5000])
except Exception as e:
    print(f'Error: {e}')

# Check file sizes of obfuscated files
print('\n\n=== Obfuscated files in inc/code/ ===')
code_dir = os.path.join(base, 'inc', 'code')
if os.path.isdir(code_dir):
    for f in sorted(os.listdir(code_dir)):
        fp = os.path.join(code_dir, f)
        size = os.path.getsize(fp)
        # Check if binary
        with open(fp, 'rb') as fh:
            head = fh.read(200)
        is_binary = b'\x00' in head or b'\xff' in head[:20]
        marker = ' [BINARY/OBFUSCATED]' if is_binary else ''
        print(f'  {size:8d} bytes  {f}{marker}')
