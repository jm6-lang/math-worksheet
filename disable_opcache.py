import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[FIX] Disable opcache and restart')

# Disable opcache in FPM config
stdin, stdout, stderr = client.exec_command("echo 'php_admin_flag[opcache.enable] = Off' >> /etc/php/8.1/fpm/pool.d/www.conf")
print('Disabled opcache for FPM')

# Remove test.php
stdin, stdout, stderr = client.exec_command('rm -f /www/wwwroot/resource_site/test.php')

# Restart
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm nginx')
time.sleep(3)

# Test
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | wc -c')
size = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage: {size} bytes')

stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | head -3')
print('Homepage:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

# Check nginx errors
stdin, stdout, stderr = client.exec_command('tail -3 /var/log/nginx/error.log')
print('Nginx:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

client.close()