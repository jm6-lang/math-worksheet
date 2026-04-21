import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 查找配置冲突 ===\n")

# 搜索所有nginx配置
print("1. 搜索所有nginx配置...")
cmd = """grep -r "skillxm" /etc/nginx/ 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 检查nginx主配置
print("\n2. nginx主配置...")
cmd = """cat /etc/nginx/nginx.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 列出所有nginx配置文件
print("\n3. 所有nginx配置文件...")
cmd = """find /etc/nginx -name "*.conf" -exec echo "=== {} ===" \\; -exec cat {} \\;"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode().strip()
# 只显示关键部分
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'server_name' in line or 'listen' in line or '===' in line:
        print(line)

ssh.close()
