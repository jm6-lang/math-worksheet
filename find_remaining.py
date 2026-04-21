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

print('查找剩余的"打赏"关键词...')
print(cmd('grep -n "打赏" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php'))

# 也检查其他模板文件
print('\n检查其他模板文件...')
print(cmd('grep -r "打赏" /www/wwwroot/resource_site/wp-content/themes/yymarket/ 2>/dev/null | head -10'))

client.close()
