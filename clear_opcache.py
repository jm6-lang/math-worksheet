import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[FIX] Clear opcache and fix empty response')

# Step 1: Clear opcache
stdin, stdout, stderr = client.exec_command('php -r "if(function_exists(\'opcache_reset\')){opcache_reset();echo \'OPcache cleared\';}else{echo \'No opcache\';}"')
print('OPcache:', stdout.read().decode('utf-8', errors='ignore').strip())

# Step 2: Create a PHP script to clear web opcache
clear_script = "<?php\nif(function_exists('opcache_reset')){opache_reset();}\nif(function_exists('opcache_invalidate')){opcache_invalidate('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', true);opcache_invalidate('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php', true);opcache_invalidate('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php', true);opcache_invalidate('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php', true);}\necho 'DONE';\n"

stdin, stdout, stderr = client.exec_command('echo "' + clear_script.replace('"', '\\"') + '" > /tmp/clear_opcache.php')
stdin, stdout, stderr = client.exec_command('php /tmp/clear_opcache.php')
print('Web opcache:', stdout.read().decode('utf-8', errors='ignore').strip())

# Step 3: Check if opcache is enabled for FPM
stdin, stdout, stderr = client.exec_command('php -m | grep -i opcache')
print('OPcache module:', stdout.read().decode('utf-8', errors='ignore').strip())

# Step 4: Check the code.php - did we corrupt it from previous session?
stdin, stdout, stderr = client.exec_command('php -l /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php 2>&1')
print('Syntax check code.php:', stdout.read().decode('utf-8', errors='ignore').strip())

stdin, stdout, stderr = client.exec_command('php -l /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php 2>&1')
print('Syntax check admin-options.php:', stdout.read().decode('utf-8', errors='ignore').strip())

stdin, stdout, stderr = client.exec_command('php -l /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php 2>&1')
print('Syntax check options-module.php:', stdout.read().decode('utf-8', errors='ignore').strip())

# Step 5: Restart PHP-FPM fully
stdin, stdout, stderr = client.exec_command('systemctl stop php8.1-fpm && sleep 1 && systemctl start php8.1-fpm')
time.sleep(2)

# Step 6: Test again
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | wc -c')
home_size = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage size: {home_size} bytes')

stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | head -3')
print('Homepage:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

client.close()