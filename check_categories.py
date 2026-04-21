import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 检查WordPress分类 ===\n")

# 列出所有分类
print("1. 列出分类...")
cmd = """cd /www/wwwroot/resource_site && wp term list category --fields=term_id,name,slug --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore'))

# 创建"网赚项目"分类
print("\n2. 创建网赚项目分类...")
cmd = """cd /www/wwwroot/resource_site && wp term create category "网赚项目" --slug="wangzhuan" --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

# 创建"创业"分类
print("\n3. 创建创业分类...")
cmd = """cd /www/wwwroot/resource_site && wp term create category "创业" --slug="chuangye" --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
