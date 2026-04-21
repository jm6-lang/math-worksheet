import paramiko, re

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

# 提取所有 Googlebot 相关 IP
ips_output = cmd("grep -i 'Googlebot' /var/log/nginx/access.log 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort -u")
ips = [ip.strip() for ip in ips_output.strip().split('\n') if ip.strip()]

print(f'=== Googlebot IP 真实性验证（共 {len(ips)} 个）===')
print()

# Google 官方爬虫 IP 段
GOOGLE_IP_PREFIXES = ['66.249.64', '66.249.65', '66.249.66', '66.249.67', '66.249.68',
                      '66.249.69', '66.249.70', '66.249.71', '66.249.72', '66.249.73',
                      '66.249.74', '66.249.75', '66.249.76', '66.249.77', '66.249.78',
                      '66.249.79', '66.249.80', '66.249.81', '66.249.82', '66.249.83',
                      '72.14.199', '74.125.', '142.250.', '172.217.', '209.85.',
                      '2001:4860:', '2607:f8b0:']

suspicious = []
real_google = []

for ip in ips:
    prefix = '.'.join(ip.split('.')[:2]) if '.' in ip else ''
    is_google_range = any(ip.startswith(p) for p in GOOGLE_IP_PREFIXES)
    
    if is_google_range:
        status = '✅ Google 官方 IP 段'
        real_google.append(ip)
    else:
        status = '⚠️ 疑似伪造!'
        suspicious.append(ip)
    
    # 反向 DNS 查询
    rdns = cmd(f'host {ip} 2>&1', timeout=10).strip()
    if 'domain name pointer' in rdns.lower() or 'pointer' in rdns.lower():
        rdns_info = rdns
    else:
        rdns_info = rdns[:80]
    
    print(f'{ip:18s} | {status}')
    print(f'                     RDNS: {rdns_info[:100]}')
    print()

print('=' * 50)
print(f'真实 Googlebot: {len(real_google)} 个 IP')
print(f'疑似伪造请求: {len(suspicious)} 个 IP')
print()
print('真实 Googlebot IP:', ', '.join(real_google[:10]))
if suspicious:
    print('疑似伪造 IP:', ', '.join(suspicious))
    print()
    print('伪造特征: 这些 IP 不是 Google 官方爬虫 IP 段')
    print('可能伪装成 Googlebot 的爬虫或扫描器，建议封禁')

# 检查 robots.txt 内容
print()
print('=== robots.txt 内容 ===')
print(cmd('curl -s http://127.0.0.1/robots.txt 2>/dev/null | head -20'))

# 检查 Baiduspider 总访问量
print()
print('=== Baiduspider 检查（扩大搜索范围）===')
print('access.log 总行数:', cmd('wc -l /var/log/nginx/access.log 2>/dev/null').strip())
print('Baiduspider 总行数:', cmd('grep -i "Baiduspider" /var/log/nginx/access.log 2>/dev/null | wc -l').strip())
print('Baiduspider-mobile 总行数:', cmd('grep -i "baidu.com" /var/log/nginx/access.log 2>/dev/null | wc -l').strip())

client.close()
