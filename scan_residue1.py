import paramiko, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)
    return client

def run_cmd(client, cmd, timeout=30):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

client = connect()

# 1. Scan for any remaining zibll/ZibAut files on the entire server
print('='*70)
print('[1] 残留zibll文件扫描（全盘）')
print('='*70)
out = run_cmd(client, 'find / -maxdepth 6 -iname "*zibll*" -o -iname "*zib_aut*" -o -iname "*ZibAut*" 2>/dev/null | grep -v "/proc\\|/sys\\|/tmp/zibll_backup"')
print(out if out else '无残留')

# 2. Scan for suspicious PHP patterns in wp-content
print('\n' + '='*70)
print('[2] wp-content目录可疑代码扫描')
print('='*70)
script = """#!/bin/bash
SITE="/www/wwwroot/resource_site"
cd "$SITE/wp-content"

# High-risk patterns scan
echo "--- eval(gzinflate ---"
grep -rl "eval\s*(\s*gzinflate" . --include="*.php" 2>/dev/null

echo "--- eval(base64_decode ---"
grep -rl "eval\s*(\s*base64_decode" . --include="*.php" 2>/dev/null

echo "--- base64_decode + eval combo ---"
grep -rl "base64_decode.*eval\|eval.*base64_decode" . --include="*.php" 2>/dev/null

echo "--- shell_exec ---"
grep -rl "shell_exec\s*(" . --include="*.php" 2>/dev/null

echo "--- system( ---"
grep -rl "\bsystem\s*\(" . --include="*.php" 2>/dev/null

echo "--- passthru ---"
grep -rl "\bpassthru\s*\(" . --include="*.php" 2>/dev/null

echo "--- proc_open ---"
grep -rl "\bproc_open\s*\(" . --include="*.php" 2>/dev/null

echo "--- popen ---"
grep -rl "\bpopen\s*\(" . --include="*.php" 2>/dev/null

echo "--- assert + eval ---"
grep -rl "assert\s*(" . --include="*.php" 2>/dev/null | head -20

echo "--- create_function ---"
grep -rl "create_function\s*(" . --include="*.php" 2>/dev/null

echo "--- preg_replace /e ---"
grep -rl "preg_replace.*['\\"][^'\\"]*[eE]['\\\"]" . --include="*.php" 2>/dev/null

echo "--- str_rot13 ---"
grep -rl "str_rot13\s*(" . --include="*.php" 2>/dev/null

echo "--- gzinflate ---"
grep -rl "gzinflate\s*(" . --include="*.php" 2>/dev/null

echo "--- gzuncompress ---"
grep -rl "gzuncompress\s*(" . --include="*.php" 2>/dev/null

echo "--- file_put_contents + eval ---"
grep -rl "file_put_contents" . --include="*.php" 2>/dev/null

echo "--- curl_multi + eval ---"
grep -rn "curl_multi" . --include="*.php" 2>/dev/null | head -20
"""

sftp = client.open_sftp()
with sftp.file('/tmp/scan2.sh', 'w') as f:
    f.write(script)
sftp.close()
out = run_cmd(client, 'bash /tmp/scan2.sh', timeout=30)
print(out)

client.close()
