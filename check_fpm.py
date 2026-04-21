import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[DEBUG] Check PHP-FPM and full response')

# Check if PHP-FPM is actually running
stdin, stdout, stderr = client.exec_command('systemctl is-active php8.1-fpm')
print(f'PHP-FPM status: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Check PHP-FPM service
stdin, stdout, stderr = client.exec_command('systemctl status php8.1-fpm --no-pager 2>&1 | head -15')
print(f'PHP-FPM detail: {stdout.read().decode("utf-8", errors="ignore").strip()[:500]}')

# Check if the socket file exists
stdin, stdout, stderr = client.exec_command('ls -la /var/run/php/php-fpm.sock 2>/dev/null || ls -la /run/php/php8.1-fpm.sock 2>/dev/null')
print(f'Socket: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Restart PHP-FPM and wait
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm 2>&1')
time.sleep(3)

# Now try curl with timeout
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | wc -c')
size = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage bytes after restart: {size}')

# Check if there's a timeout issue
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 -o /tmp/curl_test.html -w "HTTP:%{http_code} Size:%{size_download}" https://127.0.0.1/ 2>&1')
result = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Curl result: {result}')

# Check PHP-FPM error log  
stdin, stdout, stderr = client.exec_command('find /var/log -name "*php*" -o -name "*fpm*" 2>/dev/null')
print(f'PHP logs: {stdout.read().decode("utf-8", errors="ignore").strip()[:200]}')

# Check PHP-FPM specific log
stdin, stdout, stderr = client.exec_command('cat /var/log/php8.1-fpm.log 2>/dev/null | tail -10')
print(f'FPM log: {stdout.read().decode("utf-8", errors="ignore").strip()[:500]}')

client.close()