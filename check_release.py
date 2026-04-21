import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查发布配置表结构 ===\n")

# 检查表结构
print("1. skycaiji_release 表结构:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'DESC skycaiji_release;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 检查所有表
print("\n2. 所有表列表:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SHOW TABLES;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 检查provider表（可能存储发布配置）
print("\n3. skycaiji_provider 表:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'DESC skycaiji_provider;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip()[:300])

ssh.close()
