import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[FIX] Full restart and fresh test')

# Kill all PHP-FPM processes
stdin, stdout, stderr = client.exec_command('systemctl stop php8.1-fpm')
time.sleep(2)

# Verify it's stopped
stdin, stdout, stderr = client.exec_command('systemctl is-active php8.1-fpm')
print(f'FPM status: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Start fresh
stdin, stdout, stderr = client.exec_command('systemctl start php8.1-fpm')
time.sleep(3)

# Check FPM is running
stdin, stdout, stderr = client.exec_command('systemctl status php8.1-fpm --no-pager 2>&1 | grep -E "Active|pid"')
print(f'FPM: {stdout.read().decode("utf-8", errors="ignore").strip()[:200]}')

# Clear all error logs
stdin, stdout, stderr = client.exec_command('> /var/log/nginx/error.log')
stdin, stdout, stderr = client.exec_command('rm -f /www/wwwroot/resource_site/wp-content/debug.log')

# Make request and capture FULL output including stderr
stdin, stdout, stderr = client.exec_command('curl -v -k --max-time 10 https://127.0.0.1/ 2>&1')
full = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Full curl output ({len(full)} chars):')
print(full[:1500])

# Check error logs after request
time.sleep(1)
stdin, stdout, stderr = client.exec_command('cat /var/log/nginx/error.log')
print(f'Nginx errors after: {stdout.read().decode("utf-8", errors="ignore").strip()[:500]}')

stdin, stdout, stderr = client.exec_command('cat /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null')
print(f'Debug log after: {stdout.read().decode("utf-8", errors="ignore").strip()[:500]}')

client.close()