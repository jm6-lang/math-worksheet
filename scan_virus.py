import os, re

base = r'C:\Users\Administrator\Desktop\新建文件夹\zibll'
findings = []

patterns = {
    'eval(': r'\beval\s*\(',
    'base64_decode': r'base64_decode\s*\(',
    'gzinflate': r'gzinflate\s*\(',
    'gzuncompress': r'gzuncompress\s*\(',
    'str_rot13': r'str_rot13\s*\(',
    'rawurldecode': r'rawurldecode\s*\(',
    'assert(': r'\bassert\s*\(',
    'create_function': r'create_function\s*\(',
    'call_user_func': r'call_user_func(_array)?\s*\(',
    'shell_exec': r'\bshell_exec\s*\(',
    'system(': r'\bsystem\s*\(',
    'passthru': r'\bpassthru\s*\(',
    'popen': r'\bpopen\s*\(',
    'proc_open': r'\bproc_open\s*\(',
    'file_put_contents': r'file_put_contents\s*\(',
    'file_get_contents(url)': r'file_get_contents\s*\(\s*[\'"]https?://',
    'curl_exec': r'curl_exec\s*\(',
    'fsockopen': r'\bfsockopen\s*\(',
    'DOLLAR_POST/GET': r'\x24_(POST|GET|REQUEST|COOKIE)\s*\[',
    'mail(': r'\bmail\s*\(',
    'chmod': r'\bchmod\s*\(',
    'unlink': r'\bunlink\s*\(',
    'rmdir': r'\brmdir\s*\(',
    'glob': r'\bglob\s*\(',
    'scandir': r'\bscandir\s*\(',
    'move_uploaded_file': r'\bmove_uploaded_file\s*\(',
    'include($': r'include(_once)?\s*\(\s*\$',
    'require($': r'require(_once)?\s*\(\s*\$',
    'preg_replace /e': r'preg_replace\s*\(\s*[\'"][^\'"]*[\'"]\s*,\s*[\'"][^\'"]*e[\'"]',
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
