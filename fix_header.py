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

# 删除 header.php 第9-21行（损坏的通知栏残骸）
print('[1] 删除 header.php 损坏的通知栏残骸（第9-21行）...')
cmd('sed -i "9,21d" /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php')

# 验证 PHP 语法
print('\n[2] PHP 语法检查...')
print(cmd('php -l /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php'))

# 查看修复后的前15行
print('\n[3] 修复后的前15行:')
result = cmd('sed -n "1,15p" /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php')
print(result)

# 测试网站
print('\n[4] 测试网站访问...')
status = cmd('curl -s -o /dev/null -w "%{http_code}" https://www.skillxm.cn/')
print(f'HTTP状态码: {status.strip()}')

# 查看完整 HTML 前500字符
print('\n[5] 检查前端HTML前500字符...')
import urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request('https://www.skillxm.cn/', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
html = resp.read().decode('utf-8', errors='replace')
print(html[:500])

client.close()
