import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[FIX] Check and fix mu-plugin')

# Check mu-plugin
stdin, stdout, stderr = client.exec_command('ls -la /www/wwwroot/resource_site/wp-content/mu-plugins/')
print('MU plugins:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check mu-plugin syntax
stdin, stdout, stderr = client.exec_command('php -l /www/wwwroot/resource_site/wp-content/mu-plugins/zibll-bypass.php 2>&1')
print('Syntax:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check mu-plugin content
stdin, stdout, stderr = client.exec_command('cat /www/wwwroot/resource_site/wp-content/mu-plugins/zibll-bypass.php')
print('Content:', stdout.read().decode('utf-8', errors='ignore').strip())

# Try temporarily removing ALL mu-plugins
stdin, stdout, stderr = client.exec_command('mv /www/wwwroot/resource_site/wp-content/mu-plugins /www/wwwroot/resource_site/wp-content/mu-plugins.disabled')

stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')
time.sleep(2)

# Test
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | wc -c')
size = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage without mu-plugins: {size} bytes')

stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | head -5')
print('Homepage:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

client.close()