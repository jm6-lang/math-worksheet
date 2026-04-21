import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[TEST] Testing site with Host header')

# Test HTTP
stdin, stdout, stderr = client.exec_command('curl -sL http://127.0.0.1 -H "Host: skillxm.cn" | head -20')
result = stdout.read().decode('utf-8', errors='ignore').strip()
print('HTTP result:', result[:400] if result else 'EMPTY')

# Test HTTPS 
stdin, stdout, stderr = client.exec_command('curl -skL https://127.0.0.1 -H "Host: skillxm.cn" | head -20')
result2 = stdout.read().decode('utf-8', errors='ignore').strip()
print('HTTPS result:', result2[:400] if result2 else 'EMPTY')

# Check current nginx config for 443
stdin, stdout, stderr = client.exec_command('grep -A5 "listen 443" /etc/nginx/sites-available/resource_site.conf')
print('443 config:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()