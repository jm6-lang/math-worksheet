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

# === Scan 1: Residual zibll files ===
print('='*70)
print('[1] 残留zibll文件扫描')
print('='*70)
out = run_cmd(client, 'find /www/wwwroot -iname "*zibll*" -o -iname "*ZibAut*" -o -iname "*zib-aut*" 2>/dev/null')
print(out if out else '无残留')

out = run_cmd(client, 'find /tmp -iname "*zibll*" 2>/dev/null')
print(f'\n/tmp备份: {out if out else "无"}')

# === Scan 2: Suspicious PHP patterns ===
print('\n' + '='*70)
print('[2] 可疑PHP代码扫描 (wp-content)')
print('='*70)

checks = [
    ('eval+gzinflate', 'grep -rl "eval.*gzinflate\\|gzinflate.*eval" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('eval+base64', 'grep -rl "eval.*base64_decode\\|base64_decode.*eval" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('shell_exec', 'grep -rl "shell_exec" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('system()', 'grep -rl "\\\\bsystem\\\\s*(" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('passthru', 'grep -rl "passthru" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('proc_open', 'grep -rl "proc_open" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('popen', 'grep -rl "\\\\bpopen\\\\s*(" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('create_function', 'grep -rl "create_function" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('str_rot13', 'grep -rl "str_rot13" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('gzinflate', 'grep -rl "gzinflate" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('gzuncompress', 'grep -rl "gzuncompress" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('assert()', 'grep -rl "assert" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
    ('curl_exec', 'grep -rl "curl_exec" /www/wwwroot/resource_site/wp-content --include="*.php" 2>/dev/null'),
]

for name, cmd in checks:
    out = run_cmd(client, cmd)
    if out:
        print(f'\n  [{name}] 发现:')
        for line in out.split('\n'):
            print(f'    {line}')
    else:
        print(f'  [{name}] 未发现')

# === Scan 3: Recently modified files (potential backdoor planting) ===
print('\n' + '='*70)
print('[3] 近期修改的PHP文件 (可能的植入) - 最近7天')
print('='*70)
out = run_cmd(client, 'find /www/wwwroot/resource_site/wp-content -name "*.php" -mtime -7 -type f 2>/dev/null | head -40')
print(out if out else '无')

# === Scan 4: Hidden files and suspicious names ===
print('\n' + '='*70)
print('[4] 可疑隐藏文件/可疑文件名')
print('='*70)
out = run_cmd(client, 'find /www/wwwroot/resource_site/wp-content -name ".*" -type f 2>/dev/null')
print(out if out else '无隐藏文件')

out = run_cmd(client, 'find /www/wwwroot/resource_site/wp-content -name "*.php.*" -type f 2>/dev/null')
print(f'PHP备份文件: {out if out else "无"}')

out = run_cmd(client, 'find /www/wwwroot/resource_site/wp-content/uploads -name "*.php" -type f 2>/dev/null')
print(f'uploads目录中PHP文件: {out if out else "无"}')

# === Scan 5: Suspicious database options (zibll related) ===
print('\n' + '='*70)
print('[5] 数据库中zibll相关选项')
print('='*70)
out = run_cmd(client, "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_name FROM wp_options WHERE option_name LIKE '%zibll%' OR option_name LIKE '%zib_%' OR option_name LIKE '%bbs_%';\" 2>/dev/null")
if out:
    lines = out.split('\n')
    print(f'发现 {len(lines)} 个zibll相关数据库选项:')
    for l in lines[:30]:
        print(f'  {l}')
    if len(lines) > 30:
        print(f'  ... 还有 {len(lines)-30} 个')
else:
    print('无zibll相关选项')

# === Scan 6: Crontab check ===
print('\n' + '='*70)
print('[6] 定时任务检查')
print('='*70)
out = run_cmd(client, 'crontab -l 2>/dev/null')
print(out if out else '无定时任务')

out = run_cmd(client, 'ls -la /etc/cron.d/ 2>/dev/null')
print(f'\n/etc/cron.d/:\n{out}')

# === Scan 7: Suspicious processes ===
print('\n' + '='*70)
print('[7] 可疑进程')
print('='*70)
out = run_cmd(client, 'ps aux | grep -iE "miner|crypto|xmrig|masscan|zgrab|nmap|hydra|metasploit" | grep -v grep')
print(out if out else '无可疑进程')

out = run_cmd(client, 'ps aux --sort=-%cpu | head -10')
print(f'\nCPU占用TOP10:\n{out}')

client.close()
