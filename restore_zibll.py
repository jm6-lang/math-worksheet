import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[RESTORE] Zibll theme with zibpay')

# Step 1: Restore zibpay.disabled to zibpay
stdin, stdout, stderr = client.exec_command('rm -rf /www/wwwroot/resource_site/wp-content/themes/zibll/zibpay')
print('Removed empty zibpay')

stdin, stdout, stderr = client.exec_command('cp -a /www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled /www/wwwroot/resource_site/wp-content/themes/zibll/zibpay')
print('Restored zibpay from backup')

# Step 2: Restore inc.php (remove the comment we added)
stdin, stdout, stderr = client.exec_command('cp /tmp/themes_backup/inc/inc.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php 2>/dev/null')
print('Restored inc.php from backup')

# Step 3: Fix permissions
stdin, stdout, stderr = client.exec_command('chown -R www-data:www-data /www/wwwroot/resource_site/wp-content/themes/zibll/')
stdin, stdout, stderr = client.exec_command('chmod -R 755 /www/wwwroot/resource_site/wp-content/themes/zibll/')
print('Fixed permissions')

# Step 4: Switch theme back to zibll
sql = """USE wp_skillxm;
UPDATE wp_options SET option_value = 'zibll' WHERE option_name = 'template';
UPDATE wp_options SET option_value = 'zibll' WHERE option_name = 'stylesheet';
UPDATE wp_options SET option_value = 'zibll' WHERE option_name = 'current_theme';
"""

sftp = client.open_sftp()
f = sftp.file('/tmp/switch_zibll.sql', 'w')
f.write(sql)
f.close()

stdin, stdout, stderr = client.exec_command('mysql -u root < /tmp/switch_zibll.sql 2>&1')
print('Switched theme to zibll')

# Step 5: Reload PHP
stdin, stdout, stderr = client.exec_command('systemctl reload php8.1-fpm')
print('Reloaded PHP-FPM')

# Step 6: Access wp-admin to trigger create_db
stdin, stdout, stderr = client.exec_command('curl -s -k -b /tmp/cookies.txt -c /tmp/cookies.txt "https://127.0.0.1/wp-login.php" > /dev/null 2>&1')
# Login to wp-admin
stdin, stdout, stderr = client.exec_command('curl -s -k -b /tmp/cookies.txt -c /tmp/cookies.txt -d "log=admin&pwd=Admin123456&wp-submit=Log+In&redirect_to=https://127.0.0.1/wp-admin/&testcookie=1" "https://127.0.0.1/wp-login.php" -L -o /tmp/login_result.html 2>&1')
print('Attempted wp-admin login')

# Step 7: Access wp-admin page to trigger admin_head
stdin, stdout, stderr = client.exec_command('curl -s -k -b /tmp/cookies.txt "https://127.0.0.1/wp-admin/" -o /tmp/admin_page.html 2>&1')
print('Accessed wp-admin to trigger create_db')

# Step 8: Check if tables were created
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_skillxm LIKE \'%zibpay%\';"')
print('Zibpay tables after trigger:', stdout.read().decode('utf-8', errors='ignore').strip())

# Step 9: Test homepage
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ | head -20')
homepage = stdout.read().decode('utf-8', errors='ignore').strip()
print('Homepage test:', homepage[:400])

client.close()
print('[DONE]')