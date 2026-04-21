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

GOOGLE_IP_PREFIXES = ['66.249.64', '66.249.65', '66.249.66', '66.249.67', '66.249.68',
                      '66.249.69', '66.249.70', '66.249.71', '66.249.72', '66.249.73',
                      '66.249.74', '66.249.75', '66.249.76', '66.249.77', '66.249.78',
                      '66.249.79', '66.249.80', '66.249.81', '66.249.82', '66.249.83',
                      '72.14.199', '74.125.', '142.250.', '172.217.', '209.85.',
                      '2001:4860:', '2607:f8b0:']

ips_output = cmd("grep -i 'Googlebot' /var/log/nginx/access.log 2>/dev/null | grep -oE '[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+' | sort -u")
ips = [ip.strip() for ip in ips_output.strip().split('\n') if ip.strip()]

print(f'=== Googlebot IP 真实性验证（共 {len(ips)} 个）===')

suspicious = []
real_google = []

for ip in ips:
    is_google_range = any(ip.startswith(p) for p in GOOGLE_IP_PREFIXES)
    status = '[OK] Google 官方IP段' if is_google_range else '[SUSPICIOUS]'
    if is_google_range:
        real_google.append(ip)
    else:
        suspicious.append(ip)
    rdns = cmd(f'host {ip} 2>&1', timeout=10).strip()
    print(f'{ip:18s} | {status}')
    print(f'  RDNS: {rdns[:100]}')
    print()

print(f'=== 汇总 ===')
print(f'Google 官方 IP: {len(real_google)} 个 - {", ".join(real_google[:10])}')
print(f'疑似伪造 IP: {len(suspicious)} 个 - {", ".join(suspicious)}')
if suspicious:
    print()
    print('!! 警告: 以下 IP 伪装成 Googlebot，实际不是 Google 爬虫')
    for ip in suspicious:
        print(f'  {ip}')

print()
print('=== Baiduspider 总访问量 ===')
print('Baiduspider 总行数:', cmd('grep -i "Baiduspider" /var/log/nginx/access.log 2>/dev/null | wc -l').strip())
print('所有 baidu 相关:', cmd('grep -i "baidu" /var/log/nginx/access.log 2>/dev/null | wc -l').strip())
print('robots.txt 访问来自哪些IP:', cmd("grep -i 'robots.txt' /var/log/nginx/access.log 2>/dev/null | grep -oE '[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+' | sort -u | head -10").strip())

client.close()
