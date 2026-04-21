import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[DEBUG] wp-admin errors')

# Get the actual error from admin page
stdin, stdout, stderr = client.exec_command('grep -i "Fatal\\|database error\\|Warning.*require" /tmp/test_admin.html 2>/dev/null | head -5')
print('Admin errors:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check PHP error log
stdin, stdout, stderr = client.exec_command('tail -5 /var/log/php8.1-fpm.log 2>/dev/null')
print('PHP log:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

# Check nginx error log
stdin, stdout, stderr = client.exec_command('tail -5 /var/log/nginx/error.log')
print('Nginx:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Try accessing admin via PHP directly
stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/resource_site && php -r "define(WP_USE_THEMES,false); require wp-load.php; echo current_user_can(manage_options) ? ADMIN_OK : NO_ADMIN;" 2>&1')
print('PHP check:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

client.close()