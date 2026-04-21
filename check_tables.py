import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查配置并手动创建数据库表 ===\n")

# 1. 检查配置文件
print("1. 配置文件:")
cmd = """cat /www/wwwroot/skycaiji/data/config.php"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 查找SQL文件
print("\n2. 查找SQL文件:")
cmd = """find /www/wwwroot/skycaiji -name "*.sql" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
sql_files = stdout.read().decode().strip()
print(sql_files if sql_files else "未找到SQL文件")

# 3. 查看安装数据文件
print("\n3. 安装数据目录:")
cmd = """ls -la /www/wwwroot/skycaiji/vendor/skycaiji/app/install/data/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
