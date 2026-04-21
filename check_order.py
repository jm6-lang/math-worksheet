import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查Nginx配置加载顺序 ===\n")

# 1. 查看resource_site.conf内容确认顺序
print("1. 确认resource_site.conf内容...")
cmd = """head -30 /etc/nginx/sites-available/resource_site.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 测试nginx -T 看实际加载顺序
print("\n2. Nginx -T 输出（检查server块顺序）...")
cmd = """nginx -T 2>&1 | grep -A5 "server_name caiji" | head -20"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 3. 测试不带Host直接访问
print("\n3. 直接测试不带Host...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/' 2>/dev/null | head -5"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 4. 测试skycaiji目录
print("\n4. 测试skycaiji目录...")
cmd = """ls -la /www/wwwroot/skycaiji/public/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
