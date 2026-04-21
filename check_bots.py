import paramiko

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22222
user = 'root'
password = 'Langlang0.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False)

def cmd(c, timeout=60):
    stdin, stdout, stderr = client.exec_command(c, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 检查 nginx 日志文件位置
print('=== 日志文件位置 ===')
print(cmd('ls -la /www/wwwlogs/ 2>/dev/null'))
print(cmd('ls -la /var/log/nginx/ 2>/dev/null'))

# 检查 Googlebot
print('\n=== Googlebot 记录 ===')
print('--- 过去 7 天汇总 ---')
print(cmd('grep -i "Googlebot" /www/wwwlogs/*.log 2>/dev/null | wc -l'))
print(cmd('grep -i "Googlebot" /var/log/nginx/access.log 2>/dev/null | wc -l'))
print()
print('--- 最近 20 条 Googlebot ---')
print(cmd('grep -i "Googlebot" /www/wwwlogs/resource_skillxm.cn.log 2>/dev/null | tail -20'))
print(cmd('grep -i "Googlebot" /var/log/nginx/access.log 2>/dev/null | tail -20'))
print()
print('--- Googlebot IP 来源（验证真实性）---')
print(cmd('grep -i "Googlebot" /www/wwwlogs/resource_skillxm.cn.log 2>/dev/null | grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | sort | uniq -c | sort -rn | head -20'))
print(cmd('grep -i "Googlebot" /var/log/nginx/access.log 2>/dev/null | grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | sort | uniq -c | sort -rn | head -20'))

# 检查 Baiduspider
print('\n=== Baiduspider 记录 ===')
print('--- 过去 7 天汇总 ---')
print(cmd('grep -i "Baiduspider" /www/wwwlogs/*.log 2>/dev/null | wc -l'))
print(cmd('grep -i "Baiduspider" /var/log/nginx/access.log 2>/dev/null | wc -l'))
print()
print('--- 最近 20 条 Baiduspider ---')
print(cmd('grep -i "Baiduspider" /www/wwwlogs/resource_skillxm.cn.log 2>/dev/null | tail -20'))
print(cmd('grep -i "Baiduspider" /var/log/nginx/access.log 2>/dev/null | tail -20'))
print()
print('--- Baiduspider IP 来源（验证真实性）---')
print(cmd('grep -i "Baiduspider" /www/wwwlogs/resource_skillxm.cn.log 2>/dev/null | grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | sort | uniq -c | sort -rn | head -20'))
print(cmd('grep -i "Baiduspider" /var/log/nginx/access.log 2>/dev/null | grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | sort | uniq -c | sort -rn | head -20'))

# 验证爬虫 IP 真实性
print('\n=== 爬虫 IP 反向解析验证 ===')
for ip in cmd('grep -iE "Googlebot|Baiduspider" /www/wwwlogs/resource_skillxm.cn.log 2>/dev/null | grep -oE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" | sort -u').strip().split('\n'):
    if ip.strip():
        result = cmd(f'host {ip.strip()} 2>&1 || nslookup {ip.strip()} 2>&1')
        print(f'{ip}: {result.strip()[:100]}')

client.close()
