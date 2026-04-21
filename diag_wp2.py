import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

# 1. Check current active theme
print('=== Current Theme ===')
stdin, stdout, stderr = client.exec_command("mysql -u root -N -e \"SELECT option_value FROM wp_skillxm.wp_options WHERE option_name='stylesheet';\"")
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 2. Check if site responds
print('\n=== HTTP Test ===')
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 5 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 3. Check PHP error log
print('\n=== PHP Error Log (last 20) ===')
stdin, stdout, stderr = client.exec_command('tail -20 /www/server/php/81/var/log/php-fpm.log 2>&1')
log = stdout.read().decode('utf-8', errors='ignore').strip()
print(log[-1500:] if len(log) > 1500 else log)

# 4. Check WordPress debug log
print('\n=== WP debug.log (last 20) ===')
stdin, stdout, stderr = client.exec_command('tail -20 /www/wwwroot/resource_site/wp-content/debug.log 2>&1')
dbg = stdout.read().decode('utf-8', errors='ignore').strip()
if 'No such file' in dbg:
    print('No debug.log found')
else:
    print(dbg[-1500:] if len(dbg) > 1500 else dbg)

# 5. Check inc.php lines 85-95 to see what it requires
print('\n=== inc.php 85-95 ===')
stdin, stdout, stderr = client.exec_command("sed -n '85,95p' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php 2>&1")
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 6. Check functions.php to see what files it loads at init time
print('\n=== functions.php (first 50 lines) ===')
stdin, stdout, stderr = client.exec_command("head -50 /www/wwwroot/resource_site/wp-content/themes/zibll/functions.php 2>&1")
print(stdout.read().decode('utf-8', errors='ignore').strip()[:1500])

client.close()