import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[DEBUG] Check if PHP-FPM is hanging')

# Check PHP-FPM process status
stdin, stdout, stderr = client.exec_command('ps aux | grep php-fpm | grep -v grep | head -10')
print('PHP-FPM processes:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check the FPM pool configuration for max_children
stdin, stdout, stderr = client.exec_command('grep -E "pm\\.|max_children|max_requests|request_terminate" /etc/php/8.1/fpm/pool.d/www.conf')
print('Pool config:', stdout.read().decode('utf-8', errors='ignore').strip())

# Add request_terminate_timeout to prevent hanging
stdin, stdout, stderr = client.exec_command("echo 'request_terminate_timeout = 30' >> /etc/php/8.1/fpm/pool.d/www.conf")
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')
time.sleep(2)

# Now try with longer timeout
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 30 -D - https://127.0.0.1/ 2>&1')
result = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Response ({len(result)} chars):')
print(result[:2000])

client.close()