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

# 查看 header.php 完整前50行
print('[1] header.php 前50行完整内容:')
result = cmd('sed -n "1,50p" /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php')
print(result)

# 查看 footer.php 完整内容
print('\n\n[2] footer.php 完整内容:')
result = cmd('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php')
print(result)

client.close()
