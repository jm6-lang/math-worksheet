#!/usr/bin/env python3
"""
Zibll Theme Security Monitor v2
更智能的检测：区分正常用法和恶意后门
"""
import paramiko
import time
from datetime import datetime

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'
THEME_PATH = '/www/wwwroot/resource_site/wp-content/themes/zibll'
LOG_FILE = '/tmp/zibll_monitor_v2.log'

# 真正的恶意模式（后门特征）
MALICIOUS_PATTERNS = [
    ('eval.*gzinflate.*base64', 'Obfuscated backdoor (eval+gzinflate+base64)'),
    ('eval.*base64_decode.*\(', 'Encoded eval backdoor'),
    ('gzinflate.*base64_decode.*eval', 'Multi-layer obfuscated code'),
    ('\\\\$_GET.*eval', 'GET parameter backdoor'),
    ('\\\\$_POST.*eval', 'POST parameter backdoor'),
    ('shell_exec.*\\\\$_GET', 'Shell injection via GET'),
    ('system.*\\\\$_REQUEST', 'System command injection'),
    ('preg_replace.*\/e.*base64', 'Deprecated regex backdoor'),
    ('create_function.*base64', 'Dynamic function backdoor'),
    ('assert\\\\(.*\\\\$_', 'PHP assertion backdoor'),
    ('call_user_func.*\\\\$_', 'Callback backdoor'),
    ('file_put_contents.*\\\\$_', 'File write backdoor'),
    ('file_get_contents.*http', 'Remote file inclusion'),
]

# 正常用法的阈值（超过才危险）
NORMAL_PATTERNS = {
    'eval(': 100,   # 正常主题通常<100
    'base64_decode': 50,
    'gzinflate': 20,
}

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {msg}')

def check_malicious_patterns():
    """检查真正的恶意模式"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD)
    
    alerts = []
    
    for pattern, desc in MALICIOUS_PATTERNS:
        cmd = f'grep -rE "{pattern}" {THEME_PATH}/ 2>/dev/null | head -3'
        stdin, stdout, stderr = client.exec_command(cmd)
        result = stdout.read().decode('utf-8', errors='ignore').strip()
        if result:
            alerts.append(f'{desc}: {result[:200]}')
    
    client.close()
    return alerts

def check_normal_patterns():
    """检查正常模式的数量"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD)
    
    counts = {}
    for pattern, threshold in NORMAL_PATTERNS.items():
        cmd = f'grep -r "{pattern}" {THEME_PATH}/ 2>/dev/null | wc -l'
        stdin, stdout, stderr = client.exec_command(cmd)
        count = int(stdout.read().decode('utf-8', errors='ignore').strip())
        counts[pattern] = count
    
    client.close()
    return counts

def check_recent_files():
    """检查最近修改的文件"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD)
    
    # Check files modified in last 24 hours
    cmd = f'find {THEME_PATH}/ -name "*.php" -mtime -1 -type f 2>/dev/null'
    stdin, stdout, stderr = client.exec_command(cmd)
    recent = stdout.read().decode('utf-8', errors='ignore').strip()
    
    client.close()
    return recent

def main():
    log('=== Zibll Theme Security Monitor v2 ===')
    
    # Check malicious patterns
    alerts = check_malicious_patterns()
    if alerts:
        log('!!! MALICIOUS PATTERNS DETECTED !!!')
        for alert in alerts:
            log(f'  - {alert}')
        log('!!! DELETING THEME NOW !!!')
        # Delete theme
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, 22, USERNAME, PASSWORD)
        cmd = f'rm -rf {THEME_PATH}'
        stdin, stdout, stderr = client.exec_command(cmd)
        log('Theme deleted!')
        client.close()
        return
    
    # Check normal patterns
    counts = check_normal_patterns()
    log(f'Normal pattern counts: {counts}')
    
    danger_count = sum(1 for p, t in NORMAL_PATTERNS.items() if counts.get(p, 0) > t)
    
    if danger_count >= 3:
        log(f'!!! WARNING: {danger_count} patterns exceed threshold!')
    else:
        log('Status: OK - No backdoor detected')
    
    # Check recent files
    recent = check_recent_files()
    if recent:
        log(f'Recently modified files: {recent[:300]}')
    else:
        log('No recently modified files')
    
    log('=== Scan Complete ===')

if __name__ == '__main__':
    main()