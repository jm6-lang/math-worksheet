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

# 检查域名信息
print('[1] 域名 DNS 当前状态 ...')
print(cmd('dig skillxm.cn NS +short 2>/dev/null || nslookup -type=NS skillxm.cn 2>/dev/null'))

# 检查 SSL 证书
print('\n[2] SSL 证书信息 ...')
print(cmd('certbot certificates 2>/dev/null || echo "certbot 未安装或无证书"'))

# 检查当前访问 IP（从外部看）
print('\n[3] 域名解析 ...')
print(cmd('dig skillxm.cn A +short'))
print(cmd('dig skillxm.cn AAAA +short'))

client.close()
