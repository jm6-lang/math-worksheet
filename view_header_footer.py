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

# 查看 header.php 第1-60行（包含 mobile sidebar）
print('[1] header.php 移动端 sidebar 部分...')
content = cmd('sed -n "1,70p" /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php')
print(content)

# 查看 footer.php 中的 elegant-lang-switcher
print('\n\n[2] footer.php 中的语言切换器...')
result = cmd('grep -n -A 20 "elegant-lang\|lang-switcher" /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php')
print(result)

client.close()
