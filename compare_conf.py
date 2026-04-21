import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 比较配置文件差异 ===\n")

# 1. 检查实际启用的配置
print("1. 实际启用的resource_site.conf:")
cmd = """head -30 /etc/nginx/sites-enabled/resource_site.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 检查文件大小
print("\n2. 文件大小比较:")
cmd = """wc -l /etc/nginx/sites-enabled/resource_site.conf /etc/nginx/sites-available/resource_site.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. diff比较
print("\n3. 差异:")
cmd = """diff /etc/nginx/sites-enabled/resource_site.conf /etc/nginx/sites-available/resource_site.conf | head -50"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip() or "无差异")

ssh.close()
