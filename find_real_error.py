import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[DEBUG] Find the actual error')

# Check WordPress debug log
stdin, stdout, stderr = client.exec_command('cat /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null | tail -20')
debug = stdout.read().decode('utf-8', errors='ignore').strip()
print('WP debug log:', debug[:800] if debug else 'No debug.log')

# Use PHP CLI to test loading WordPress
stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/resource_site && php -r "define(WP_USE_THEMES, true); require_once \"wp-load.php\";" 2>&1 | tail -20')
wp_load = stdout.read().decode('utf-8', errors='ignore').strip()
print('WP load:', wp_load[:800])

# Check nginx error after the restart
stdin, stdout, stderr = client.exec_command('tail -5 /var/log/nginx/error.log')
nginx = stdout.read().decode('utf-8', errors='ignore').strip()
print('Nginx:', nginx[:500])

# Try with display errors ON in curl
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/?display_errors=1" 2>&1 | head -20')
print('With debug:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

client.close()