import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Enable display_errors and fix white page')

# Enable PHP error display in php.ini
stdin, stdout, stderr = client.exec_command("php -i | grep 'php.ini'")
phpini = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'PHP ini: {phpini}')

# Find the actual php.ini for fpm
stdin, stdout, stderr = client.exec_command("php -r \"echo php_ini_loaded_file();\"")
ini_path = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Loaded ini: {ini_path}')

# Add display_errors to PHP-FPM pool config
stdin, stdout, stderr = client.exec_command("grep -n 'display_errors\\|php_admin_value\\|php_value' /etc/php/8.1/fpm/pool.d/www.conf 2>/dev/null | head -10")
pool_config = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Pool config: {pool_config[:300]}')

# Add display_errors = On to wp-config.php before the ABSPATH line
stdin, stdout, stderr = client.exec_command("sed -i '/\\/\\*\\! That.*all, stop editing/i ini_set(\"display_errors\", 1);\\nini_set(\"display_startup_errors\", 1);\\nerror_reporting(E_ALL);' /www/wwwroot/resource_site/wp-config.php")
print('Added error display to wp-config')

# Now check the actual admin-options.php line 11090 - did our sed work?
stdin, stdout, stderr = client.exec_command("sed -n '11088,11092p' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php")
print('Line 11090:', stdout.read().decode('utf-8', errors='ignore').strip())

# If sed didn't work, do it with Python
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php', 'r')
content = f.read().decode('utf-8', errors='replace')
f.close()

if 'ZibAut::is_update()' in content:
    content = content.replace('ZibAut::is_update()', 'null /* bypassed */')
    f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php', 'w')
    f.write(content)
    f.close()
    print('Replaced ZibAut::is_update() in admin-options.php')
else:
    print('No ZibAut::is_update() found in admin-options.php')

# Fix options-module.php too
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php', 'r')
content2 = f.read().decode('utf-8', errors='replace')
f.close()

if 'ZibAut::is_update()' in content2:
    content2 = content2.replace('ZibAut::is_update()', 'null /* bypassed */')
    f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php', 'w')
    f.write(content2)
    f.close()
    print('Replaced ZibAut::is_update() in options-module.php')
else:
    print('No ZibAut::is_update() found in options-module.php')

# Fix permissions
stdin, stdout, stderr = client.exec_command('chown www-data:www-data /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php /www/wwwroot/resource_site/wp-config.php')

# Restart
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm nginx')

import time
time.sleep(1)

# Test
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | head -5')
print('Homepage:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/wp-admin/ 2>&1 | head -5')
print('Admin:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

client.close()