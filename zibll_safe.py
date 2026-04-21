#!/usr/bin/env python3
"""
Zibll Theme Security Monitor v2
更智能的检测：区分正常用法和恶意后门
"""
import paramiko
import re
from datetime import datetime

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'
THEME_PATH = '/www/wwwroot/resource_site/wp-content/themes/zibll'
LOG_FILE = '/tmp/zibll_monitor_v2.log'

# 真正的恶意模式（后门特征）
MALICIOUS_PATTERNS = [
    'eval.*gzinflate',
    'eval.*base64_decode.*eval',
    'gzinflate.*base64_decode.*eval',
]

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {msg}')

def check_malicious_files():
    """检查可能包含恶意代码的文件"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD)
    
    # Check files with suspicious patterns
    alerts = []
    
    # Check for files with eval+gzinflate combo
    stdin, stdout, stderr = client.exec_command(f'grep -rl "eval.*gzinflate\\|gzinflate.*eval" {THEME_PATH}/ 2>/dev/null')
    files = stdout.read().decode('utf-8', errors='ignore').strip()
    if files:
        alerts.append(f'eval+gzinflate in files: {files[:200]}')
    
    # Check for suspicious long base64 strings
    stdin, stdout, stderr = client.exec_command(f'grep -rEl "[A-Za-z0-9+=/]{{200,}}" {THEME_PATH}/inc/code/ 2>/dev/null | head -5')
    encoded = stdout.read().decode('utf-8', errors='ignore').strip()
    if encoded:
        alerts.append(f'Large encoded strings in: {encoded[:200]}')
    
    client.close()
    return alerts

def check_normal_counts():
    """检查正常模式的数量"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD)
    
    counts = {}
    
    stdin, stdout, stderr = client.exec_command(f'grep -r "eval(" {THEME_PATH}/ 2>/dev/null | wc -l')
    counts['eval'] = int(stdout.read().decode('utf-8', errors='ignore').strip())
    
    stdin, stdout, stderr = client.exec_command(f'grep -r "base64_decode" {THEME_PATH}/ 2>/dev/null | wc -l')
    counts['base64'] = int(stdout.read().decode('utf-8', errors='ignore').strip())
    
    stdin, stdout, stderr = client.exec_command(f'grep -r "gzinflate" {THEME_PATH}/ 2>/dev/null | wc -l')
    counts['gzinflate'] = int(stdout.read().decode('utf-8', errors='ignore').strip())
    
    client.close()
    return counts

def check_recent_modifications():
    """检查最近修改的文件"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD)
    
    # Files modified in last 24 hours
    stdin, stdout, stderr = client.exec_command(f'find {THEME_PATH}/ -name "*.php" -mtime -1 -type f 2>/dev/null')
    recent = stdout.read().decode('utf-8', errors='ignore').strip()
    
    client.close()
    return recent

def main():
    log('=== Zibll Theme Security Monitor v2 ===')
    
    # Check malicious patterns
    alerts = check_malicious_files()
    
    # Check normal pattern counts
    counts = check_normal_counts()
    log(f'Pattern counts: eval={counts["eval"]}, base64={counts["base64"]}, gzinflate={counts["gzinflate"]}')
    
    # Decision logic
    if alerts:
        log('!!! MALICIOUS PATTERNS DETECTED !!!')
        for alert in alerts:
            log(f'  - {alert}')
        
        # Only delete if truly malicious
        if 'eval+gzinflate' in str(alerts):
            log('!!! CONFIRMED BACKDOOR - DELETING THEME !!!')
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(HOST, 22, USERNAME, PASSWORD)
            cmd = f'rm -rf {THEME_PATH}'
            stdin, stdout, stderr = client.exec_command(cmd)
            log('Theme deleted!')
            client.close()
            return
    
    # Check thresholds - official theme has lots of eval but NOT in dangerous combinations
    # zibll 7.8 official has about 30-50 eval calls, not eval+gzinflate combo
    is_dangerous = (counts['eval'] > 100) or (counts['gzinflate'] > 50 and counts['eval'] > 30)
    
    if is_dangerous:
        log('!!! WARNING: Pattern counts exceed safe threshold!')
    else:
        log('Status: OK - Safe threshold')
    
    # Check recent files
    recent = check_recent_modifications()
    if recent:
        log(f'Recently modified: {recent[:200]}')
    else:
        log('No recent modifications')
    
    log('=== Scan Complete ===')

if __name__ == '__main__':
    main()