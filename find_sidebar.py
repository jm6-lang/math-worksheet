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

# 搜索所有 PHP 文件中的 sidebar 相关代码
print('[1] 搜索 sidebar 相关文件...')
result = cmd('grep -r "sidebar" /www/wwwroot/resource_site/wp-content/themes/yymarket/ --include="*.php" -l 2>/dev/null | head -10')
print(result)

# 搜索 elegant-lang-switcher
print('\n[2] 搜索语言切换器...')
result = cmd('grep -r "elegant-lang" /www/wwwroot/resource_site/wp-content/themes/yymarket/ -l 2>/dev/null')
print(result)

result = cmd('grep -r "lang-switcher" /www/wwwroot/resource_site/wp-content/themes/yymarket/ -l 2>/dev/null')
print(result)

# 搜索 sidebar.php 或相关文件
print('\n[3] 侧边栏文件...')
result = cmd('find /www/wwwroot/resource_site/wp-content/themes/yymarket/ -name "*sidebar*" -o -name "*mobile*" 2>/dev/null | grep -i php')
print(result)

# 搜索 header.php 中的移动端 sidebar
print('\n[4] 在 header.php 中搜索 sidebar...')
result = cmd('grep -n "sidebar\|mobile\|elegant-lang" /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php 2>/dev/null | head -20')
print(result)

client.close()
