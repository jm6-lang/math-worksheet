#!/usr/bin/env python3
"""
Zibll Theme Security Monitor
自动监控主题文件，发现异常自动删除
"""
import paramiko
import time
import os
from datetime import datetime

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'
THEME_PATH = '/www/wwwroot/resource_site/wp-content/themes/zibll'
LOG_FILE = '/tmp/zibll_monitor.log'

# 危险特征列表
DANGER_PATTERNS = [
    ('eval(', 'eval() execution'),
    ('base64_decode', 'Base64 decoding'),
    ('gzinflate', 'Data decompression'),
    ('str_rot13', 'ROT13 obfuscation'),
    ('shell_exec', 'Shell execution'),
    ('system(', 'System command'),
    ('passthru', 'Command execution'),
    ('exec(', 'Command execution'),
    ('preg_replace.*/e', 'Dynamic code execution'),
    ('create_function', 'Dynamic function'),
]

ALERT_THRESHOLD = 5  # 超过此数量则危险

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f'[{timestamp}] {msg}'
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def scan_theme():
    """扫描主题文件"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD)
    
    findings = {}
    
    for pattern, desc in DANGER_PATTERNS:
        cmd = f'grep -r "{pattern}" {THEME_PATH}/ 2>/dev/null | wc -l'
        stdin, stdout, stderr = client.exec_command(cmd)
        count = int(stdout.read().decode('utf-8', errors='ignore').strip())
        if count > 0:
            findings[desc] = count
    
    client.close()
    return findings

def delete_theme():
    """删除主题"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD)
    
    # Backup first
    backup_name = f'/tmp/zibll_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.tar.gz'
    cmd = f'tar -czf {backup_name} -C /www/wwwroot/resource_site/wp-content/themes zibll'
    stdin, stdout, stderr = client.exec_command(cmd)
    log(f'Backup created: {backup_name}')
    
    # Delete theme
    cmd = f'rm -rf {THEME_PATH}'
    stdin, stdout, stderr = client.exec_command(cmd)
    log('Theme deleted!')
    
    # Deactivate in database
    cmd = 'mysql -u root -e "UPDATE wp_resource.wp_options SET option_value=\'twentytwentyfour\' WHERE option_name=\'template\' OR option_name=\'stylesheet\';"'
    stdin, stdout, stderr = client.exec_command(cmd)
    
    client.close()

def main():
    log('=== Zibll Theme Security Monitor Started ===')
    
    findings = scan_theme()
    
    total_danger = sum(findings.values())
    log(f'Scan complete. Findings: {findings}')
    log(f'Total danger signals: {total_danger}')
    
    if total_danger >= ALERT_THRESHOLD:
        log('!!! ALERT: Too many danger signals detected!')
        log('!!! Deleting theme in 10 seconds...')
        time.sleep(10)
        delete_theme()
    else:
        log('Status: OK (within safe threshold)')
        # Check for new suspicious files
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, 22, USERNAME, PASSWORD)
        
        # Check recently modified PHP files
        cmd = f'find {THEME_PATH}/ -name "*.php" -mmin -60 -type f'
        stdin, stdout, stderr = client.exec_command(cmd)
        recent = stdout.read().decode('utf-8', errors='ignore').strip()
        
        if recent:
            log(f'Warning: Recently modified PHP files detected: {recent[:200]}')
        
        client.close()

if __name__ == '__main__':
    main()