import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 检查用户角色 ===\n")

# 检查用户角色
print("1. 检查admin用户...")
cmd = """cd /www/wwwroot/resource_site && wp user get 3 --allow-root --fields=ID,user_login,user_email,roles 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore'))

# 检查所有用户
print("\n2. 所有用户...")
cmd = """cd /www/wwwroot/resource_site && wp user list --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore'))

# 尝试给admin用户添加编辑权限
print("\n3. 检查用户meta...")
cmd = """mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "SELECT ID, user_login, user_email FROM wp_users;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
