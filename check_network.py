import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Network and DNS')

# Check server IP
stdin, stdout, stderr = client.exec_command('curl -s ifconfig.me 2>/dev/null || curl -s ip.sb 2>/dev/null')
print(f'Server IP: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Check DNS for skillxm.cn
stdin, stdout, stderr = client.exec_command('dig +short skillxm.cn 2>/dev/null || nslookup skillxm.cn 2>/dev/null | grep Address | tail -1')
print(f'DNS resolves to: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Check if nginx is listening on 443
stdin, stdout, stderr = client.exec_command('ss -tlnp | grep -E ":443|:80"')
print(f'Ports: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Check nginx config for skillxm.cn
stdin, stdout, stderr = client.exec_command('nginx -T 2>/dev/null | grep -A 10 "server_name.*skillxm"')
print(f'Nginx config: {stdout.read().decode("utf-8", errors="ignore").strip()[:500]}')

# Check firewall
stdin, stdout, stderr = client.exec_command('iptables -L -n 2>/dev/null | grep -E "443|80|DROP|REJECT" | head -5')
print(f'Firewall: {stdout.read().decode("utf-8", errors="ignore").strip()[:300]}')

# Check external access
stdin, stdout, stderr = client.exec_command('curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 https://skillxm.cn/ 2>&1')
print(f'External access: {stdout.read().decode("utf-8", errors="ignore").strip()}')

client.close()