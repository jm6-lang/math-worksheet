import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Use sed to replace the line')

# Use sed to comment out the is_update call
stdin, stdout, stderr = client.exec_command("sed -i \"s/\\$is_update_data = ZibAut::is_update();/\\$is_update_data = null; \\/\\/ bypassed/\" /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php")
print('Sed result:', stdout.read().decode('utf-8', errors='ignore').strip())

# Also check new_aut.php for the same pattern
stdin, stdout, stderr = client.exec_command("grep -n 'is_update\\|ZibAut' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/new_aut.php 2>/dev/null | head -10")
print('new_aut.php refs:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check if there are other files calling is_update
stdin, stdout, stderr = client.exec_command("grep -rn 'ZibAut::is_update\\|ZibAut::curl_update\\|->is_update()\\|->curl_update()' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' 2>/dev/null | grep -v 'code.php' | head -10")
print('Other is_update calls:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Fix permissions
stdin, stdout, stderr = client.exec_command('chown www-data:www-data /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php')
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')

# Test
stdin, stdout, stderr = client.exec_command('sleep 1 && curl -s -k "https://127.0.0.1/wp-admin/" -o /tmp/test_sed_admin.html -w "%{http_code}" 2>&1')
admin_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'wp-admin HTTP: {admin_code}')

stdin, stdout, stderr = client.exec_command('grep -c "Fatal" /tmp/test_sed_admin.html 2>/dev/null')
fatal = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Fatal errors: {fatal}')

stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/" -o /dev/null -w "%{http_code}" 2>&1')
home = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage HTTP: {home}')

client.close()