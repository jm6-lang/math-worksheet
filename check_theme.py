import paramiko

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22
user = 'root'
password = 'Langlang0.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False,
               banner_timeout=20, auth_timeout=20)

def cmd(c):
    stdin, stdout, stderr = client.exec_command(c, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 检查网站程序
print('[1] 检查网站根目录 ...')
print(cmd('ls -la /www/wwwroot/resource_site/'))

# 检查是否 WordPress
print('\n[2] 检查 wp-config.php ...')
print(cmd('ls /www/wwwroot/resource_site/wp-config.php 2>/dev/null && echo "WordPress 站点" || echo "非 WordPress"'))

# 检查主题
print('\n[3] WordPress 主题 ...')
print(cmd('ls /www/wwwroot/resource_site/wp-content/themes/ 2>/dev/null'))

# 搜索"打赏"相关代码
print('\n[4] 搜索打赏相关代码 ...')
print(cmd('grep -r "打赏" /www/wwwroot/resource_site/wp-content/themes/ 2>/dev/null | head -20'))

# 检查主题 functions.php
print('\n[5] 主题 functions.php 位置 ...')
print(cmd('find /www/wwwroot/resource_site/wp-content/themes/ -name "functions.php" 2>/dev/null'))

client.close()
