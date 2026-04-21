import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Replace all ZibAut::is_update calls')

# Fix options-module.php
stdin, stdout, stderr = client.exec_command("sed -i \"s/ZibAut::is_update()/null \\/\\/ bypassed/g\" /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php")
print('Fixed options-module.php')

# Verify
stdin, stdout, stderr = client.exec_command("grep -n 'is_update' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php | head -5")
print('Verify:', stdout.read().decode('utf-8', errors='ignore').strip())

# Also disable the csf_save hook from new_aut.php by commenting out the whole line
# Actually, let's just comment out the entire new_aut.php line
stdin, stdout, stderr = client.exec_command("sed -i '15s/^/\\/\\/ /' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/new_aut.php")
print('Disabled new_aut.php hooks')

# Fix permissions
stdin, stdout, stderr = client.exec_command('chown www-data:www-data /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/new_aut.php')

# Restart PHP
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')

# Test
stdin, stdout, stderr = client.exec_command('sleep 1 && curl -s -k "https://127.0.0.1/wp-admin/" -o /tmp/test_final2.html -w "%{http_code}" 2>&1')
admin_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'wp-admin HTTP: {admin_code}')

stdin, stdout, stderr = client.exec_command('grep -c "Fatal" /tmp/test_final2.html 2>/dev/null')
fatal = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Fatal errors: {fatal}')

# Check for specific error
stdin, stdout, stderr = client.exec_command('grep -i "fatal\\|error" /tmp/test_final2.html 2>/dev/null | head -3')
print('Errors:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Homepage
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/" -o /dev/null -w "%{http_code}" 2>&1')
home = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage HTTP: {home}')

# Login page
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-login.php" -o /dev/null -w "%{http_code}" 2>&1')
login = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Login HTTP: {login}')

client.close()