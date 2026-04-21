import paramiko
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 查看 WordPress 配置
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/skillxm.cn/public/wp-config.php')
content = stdout.read().decode()

db_name = re.search(r"define\s*\(\s*'DB_NAME'\s*,\s*'([^']+)'", content)
db_user = re.search(r"define\s*\(\s*'DB_USER'\s*,\s*'([^']+)'", content)
db_pass = re.search(r"define\s*\(\s*'DB_PASSWORD'\s*,\s*'([^']+)'", content)
db_host = re.search(r"define\s*\(\s*'DB_HOST'\s*,\s*'([^']+)'", content)

print('=== WordPress 数据库配置 ===')
print(f'DB_NAME: {db_name.group(1) if db_name else "N/A"}')
print(f'DB_USER: {db_user.group(1) if db_user else "N/A"}')
print(f'DB_PASSWORD: {db_pass.group(1) if db_pass else "N/A"}')
print(f'DB_HOST: {db_host.group(1) if db_host else "N/A"}')

# 查看主题
stdin, stdout, stderr = ssh.exec_command('ls /www/wwwroot/skillxm.cn/public/wp-content/themes/')
print()
print('=== 已安装主题 ===')
print(stdout.read().decode())

# 查看分类
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/skillxm.cn/public/wp-config.php | grep table_prefix')
print('=== 表前缀 ===')
print(stdout.read().decode())

ssh.close()
