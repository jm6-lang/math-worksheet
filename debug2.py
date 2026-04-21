import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查skycaiji目录 ===\n")

# 1. skycaiji public目录
print("1. skycaiji public目录...")
cmd = """ls -la /www/wwwroot/skycaiji/public/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. skycaiji index.php
print("\n2. skycaiji public/index.php...")
cmd = """cat /www/wwwroot/skycaiji/public/index.php"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. 直接用PHP测试
print("\n3. 直接运行skycaiji index.php...")
cmd = """cd /www/wwwroot/skycaiji && php -r "echo 'PHP OK';" 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 检查PHP-FPM socket
print("\n4. PHP-FPM socket...")
cmd = """ls -la /run/php/php8.1-fpm.sock 2>/dev/null || ls -la /var/run/php/php8.1-fpm.sock 2>/dev/null || echo "Socket not found" """
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 5. 检查默认Nginx站点
print("\n5. 检查default站点...")
cmd = """cat /etc/nginx/sites-available/default 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
