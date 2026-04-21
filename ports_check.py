import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] PHP and ports')

# Check if PHP files are readable
stdin, stdout, stderr = client.exec_command('ls -la /www/wwwroot/resource_site/index.php')
print('index.php:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check what ports are listening
stdin, stdout, stderr = client.exec_command('ss -tlnp')
print('Listening ports:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Test nginx status
stdin, stdout, stderr = client.exec_command('systemctl status nginx | head -10')
print('Nginx status:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

client.close()