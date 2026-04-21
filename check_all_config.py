import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查所有Nginx配置 ===\n")

# 1. 检查sites-available所有文件
print("1. 所有可用站点...")
cmd = """ls -la /etc/nginx/sites-available/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 检查sites-enabled
print("\n2. 已启用站点...")
cmd = """ls -la /etc/nginx/sites-enabled/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. 查看skillxm.cn.conf
print("\n3. skillxm.cn.conf内容...")
cmd = """cat /etc/nginx/sites-available/skillxm.cn.conf 2>/dev/null | head -50"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 搜索所有包含caiji的配置
print("\n4. 搜索caiji配置...")
cmd = """grep -r "caiji" /etc/nginx/ 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip() or "未找到")

# 5. 检查resource_site.conf的caiji部分
print("\n5. 检查resource_site.conf中是否有caiji...")
cmd = """grep -A5 "caiji" /etc/nginx/sites-available/resource_site.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip() or "未找到")

ssh.close()
