import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查PHP-FPM Socket ===\n")

# 1. PHP-FPM配置
print("1. PHP-FPM配置...")
cmd = """grep -E "listen|" /etc/php/8.1/fpm/pool.d/www.conf | head -5"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 检查socket文件
print("\n2. Socket文件...")
cmd = """ls -la /run/php/ 2>/dev/null || ls -la /var/run/php/ 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. nginx配置的socket
print("\n3. nginx配置的socket...")
cmd = """grep "fastcgi_pass" /etc/nginx/sites-available/resource_site.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 直接测试skycaiji的PHP输出
print("\n4. 直接测试skycaiji index.php...")
cmd = """cd /www/wwwroot/skycaiji && php -r 'echo "Test OK\n";' """
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 5. 用PHP内置服务器测试skycaiji
print("\n5. PHP内置服务器测试...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/skycaiji && timeout 5 php -S 127.0.0.1:8888 index.php &>/dev/null &", timeout=10)
ssh.exec_command("sleep 2", timeout=5)
cmd = """curl -sL --max-time 5 'http://127.0.0.1:8888/' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
content = stdout.read().decode('utf-8', errors='ignore')
print("PHP内置服务器响应:", content[:500])

ssh.close()
