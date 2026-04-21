import paramiko
import sys
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 完整配置天空采集器 ===\n")

# 1. 检查安装目录
print("1. 检查源码...")
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/skycaiji/ | head -15", timeout=10)
print(stdout.read().decode().strip())

# 2. 查看安装向导需要的文件
print("\n2. 检查安装向导...")
cmd = """ls -la /www/wwwroot/skycaiji/app/install/ 2>/dev/null || ls -la /www/wwwroot/skycaiji/data/ 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. 查看数据库配置文件模板
print("\n3. 检查配置文件...")
cmd = """find /www/wwwroot/skycaiji -name "*.php" | xargs grep -l "dbname\|DB_NAME\|database" 2>/dev/null | head -5"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
files = stdout.read().decode().strip()
print("数据库相关文件:", files)

# 4. 查看入口文件
print("\n4. 查看index.php...")
cmd = """cat /www/wwwroot/skycaiji/index.php"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 5. 查看配置目录结构
print("\n5. 目录结构...")
cmd = """find /www/wwwroot/skycaiji -maxdepth 2 -type d | head -20"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
