import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 直接测试skycaiji PHP ===\n")

# 1. 直接运行skycaiji index.php
print("1. 直接运行skycaiji index.php...")
cmd = """cd /www/wwwroot/skycaiji && php index.php 2>&1 | head -50"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode().strip())

# 2. 用curl测试带Host头
print("\n2. 带Host头测试...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/index.php' -H 'Host: caiji.skillxm.cn' 2>/dev/null | head -30"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print("响应:", content[:500])

# 3. 检查PHP-FPM日志
print("\n3. PHP-FPM日志...")
cmd = """tail -20 /var/log/php8.1-fpm.log 2>/dev/null || tail -20 /var/log/php-fpm.log 2>/dev/null || echo "无日志" """
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 检查nginx error log
print("\n4. Nginx错误日志...")
cmd = """tail -20 /var/log/nginx/error.log 2>/dev/null | tail -10"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
