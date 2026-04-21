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

# 查看 home-1.php 中打赏相关的代码
print('[1] 打赏板块上下文 ...')
print(cmd('grep -n -A5 -B5 "打赏" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php'))

# 查看整个 home-1.php（找打赏板块的 HTML 结构）
print('\n[2] home-1.php 完整内容（找打赏区块）...')
print(cmd('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php'))

client.close()
