import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查skycaiji文件 ===\n")

# 1. 查找所有PHP文件
print("1. 查找PHP文件...")
cmd = """find /www/wwwroot/skycaiji -name "*.php" | head -30"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 检查根目录
print("\n2. skycaiji根目录...")
cmd = """ls -la /www/wwwroot/skycaiji/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. 检查index.php
print("\n3. 查找index.php...")
cmd = """find /www/wwwroot/skycaiji -name "index.php" """
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 检查public目录所有文件
print("\n4. public目录所有文件...")
cmd = """find /www/wwwroot/skycaiji/public -type f"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
