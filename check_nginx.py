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

# 查看现有 nginx 配置
print('[1] 检查现有 nginx 配置...')
print(cmd('cat /etc/nginx/nginx.conf'))
print('\n--- conf.d 目录 ---')
print(cmd('ls -la /etc/nginx/conf.d/'))
print(cmd('cat /etc/nginx/conf.d/*.conf 2>/dev/null'))
print('\n--- sites-enabled ---')
print(cmd('ls -la /etc/nginx/sites-enabled/ 2>/dev/null'))
print(cmd('cat /etc/nginx/sites-enabled/* 2>/dev/null'))

client.close()
