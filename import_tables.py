import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 导入数据库表 ===\n")

# 1. 查看install_table文件
print("1. 查看install_table文件...")
cmd = """head -100 /www/wwwroot/skycaiji/vendor/skycaiji/app/install/data/install_table"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip()[:500])

# 2. 导入数据库
print("\n2. 导入数据库表...")
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji < /www/wwwroot/skycaiji/vendor/skycaiji/app/install/data/install_table 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode().strip()
print(result if result else "导入成功!")

# 3. 检查表
print("\n3. 检查数据库表...")
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' -e "USE skycaiji; SHOW TABLES;" 2>/dev/null | head -20"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
tables = stdout.read().decode().strip()
print(tables[:500] if tables else "无表")

ssh.close()
