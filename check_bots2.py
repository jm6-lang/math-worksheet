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

# 检查高访问量 IP 的具体行为
high_ips = ['39.171.166.233', '6.6.5.788', '43.103.5.46', '146.0.0.0', '130.0.0.0']
for ip in high_ips:
    print(f'\n=== IP: {ip} 详细行为 ===')
    print(cmd(f"grep '{ip}' /var/log/nginx/access.log 2>/dev/null | head -5"))
    print('  UA:', cmd(f"grep '{ip}' /var/log/nginx/access.log 2>/dev/null | awk -F'\"' '{{print $6}}' | sort -u | head -3"))

# 百度真实爬虫检查（百度用的是 180.76.76.x 或 119.84.x.x）
print('\n\n=== 百度真实爬虫 IP 段检查 ===')
print(cmd("grep -i 'baidu' /var/log/nginx/access.log 2>/dev/null | grep -oE '[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}' | sort -u | head -20"))

# Palo Alto Xpanse 详细行为
print('\n=== Palo Alto Networks Xpanse 扫描详情 ===')
print(cmd("grep -i 'Palo Alto' /var/log/nginx/access.log 2>/dev/null | head -10"))

# Go-http-client 详情
print('\n=== Go-http-client 爬虫详情 ===')
print(cmd("grep 'Go-http-client' /var/log/nginx/access.log 2>/dev/null | head -10"))

# 检查 WordPress 自己的爬虫行为
print('\n=== WordPress 站点自身爬取详情 ===')
print('IP 来源:', cmd("grep 'WordPress' /var/log/nginx/access.log 2>/dev/null | grep -oE '[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}' | sort -u | head -10"))
print('访问路径:', cmd("grep 'WordPress' /var/log/nginx/access.log 2>/dev/null | awk -F'\"' '{print $2}' | sort -u | head -10"))

# 假 Googlebot 伪装者的具体行为
print('\n=== 假 Googlebot（国产 IP）的具体爬取内容 ===')
fake_bots = ['49.71.119.16', '175.167.5.43', '123.180.172.166', '116.140.53.125',
             '113.76.53.30', '122.241.66.106', '183.7.117.219', '146.0.7680.177']
for ip in fake_bots:
    count = cmd(f"grep '{ip}' /var/log/nginx/access.log 2>/dev/null | wc -l").strip()
    if count and int(count) > 0:
        print(f'\n{ip} ({count}次):')
        print('  ', cmd(f"grep '{ip}' /var/log/nginx/access.log 2>/dev/null | awk -F'\"' '{{print $2}}' | head -5").strip())
        print('  UA:', cmd(f"grep '{ip}' /var/log/nginx/access.log 2>/dev/null | awk -F'\"' '{{print $6}}' | sort -u").strip())

client.close()
