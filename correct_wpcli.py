import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 创建应用密码 ===\n")

# 正确的WP-CLI命令
print("1. 创建应用密码...")
cmd = """cd /www/wwwroot/resource_site && wp user application-password create admin --name="Auto-Collect" --format=json --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

# 列出所有应用密码
print("\n2. 列出应用密码...")
cmd = """cd /www/wwwroot/resource_site && wp user application-password list admin --format=json --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:500])

ssh.close()
