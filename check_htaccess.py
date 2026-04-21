import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查天空采集器结构 ===\n")

# 1. 查看public/htaccess-nginx
print("1. public/htaccess-nginx...")
cmd = """cat /www/wwwroot/skycaiji/public/htaccess-nginx"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 查看根目录index.php
print("\n2. 根目录index.php...")
cmd = """cat /www/wwwroot/skycaiji/index.php"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. 查看README
print("\n3. README.md...")
cmd = """cat /www/wwwroot/skycaiji/README.md"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
