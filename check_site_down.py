import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Site status')

# Test homepage
stdin, stdout, stderr = client.exec_command('curl -s -k -o /dev/null -w "%{http_code}" https://127.0.0.1/ 2>&1')
print(f'Homepage HTTP: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Test wp-login
stdin, stdout, stderr = client.exec_command('curl -s -k -o /dev/null -w "%{http_code}" https://127.0.0.1/wp-login.php 2>&1')
print(f'Login HTTP: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Check PHP-FPM status
stdin, stdout, stderr = client.exec_command('systemctl status php8.1-fpm --no-pager | head -5')
print(f'PHP-FPM: {stdout.read().decode("utf-8", errors="ignore").strip()[:200]}')

# Check nginx status
stdin, stdout, stderr = client.exec_command('systemctl status nginx --no-pager | head -5')
print(f'Nginx: {stdout.read().decode("utf-8", errors="ignore").strip()[:200]}')

# Latest errors
stdin, stdout, stderr = client.exec_command('tail -5 /var/log/nginx/error.log')
print(f'Nginx errors: {stdout.read().decode("utf-8", errors="ignore").strip()[:500]}')

# Try restarting both services
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm nginx')
print('Restarted services')

# Test again
stdin, stdout, stderr = client.exec_command('curl -s -k -o /dev/null -w "%{http_code}" https://127.0.0.1/ 2>&1')
print(f'Homepage after restart: {stdout.read().decode("utf-8", errors="ignore").strip()}')

client.close()