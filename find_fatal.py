import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[DEBUG] Find the fatal error')

# Clear debug.log
stdin, stdout, stderr = client.exec_command('> /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null')

# Make a request
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ > /dev/null 2>&1')
time.sleep(1)

# Check debug.log
stdin, stdout, stderr = client.exec_command('cat /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null | tail -30')
debug = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Debug log: {debug[:1000] if debug else "EMPTY"}')

# Check PHP-FPM error log (might have separate error log for FPM workers)
stdin, stdout, stderr = client.exec_command('find /var/log -name "*fpm*" -o -name "*php*error*" 2>/dev/null')
print('Log files:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

# Check nginx error log after the request
stdin, stdout, stderr = client.exec_command('tail -5 /var/log/nginx/error.log')
print('Nginx errors:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Try loading WordPress via CLI to see the error
stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/resource_site && php -r "define(\\\"WP_USE_THEMES\\\",false); require \\\"wp-load.php\\\"; echo \\\"OK\\\";" 2>&1 | head -20')
cli_result = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'CLI WP load: {cli_result[:500]}')

client.close()