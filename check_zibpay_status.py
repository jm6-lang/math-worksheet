import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Zibpay backup and theme status')

# Check if zibpay.disabled folder exists (from earlier)
stdin, stdout, stderr = client.exec_command('ls -la /www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/ 2>/dev/null')
print('Zibpay disabled backup:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

# Check current zibpay folder
stdin, stdout, stderr = client.exec_command('ls -la /www/wwwroot/resource_site/wp-content/themes/zibll/zibpay/ 2>/dev/null')
print('Current zibpay:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

# Check theme backup
stdin, stdout, stderr = client.exec_command('ls -la /tmp/zibll_backup_20260405_194507.tar.gz')
print('Backup exists:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check what databases exist
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW DATABASES;"')
print('Databases:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check wp_resource for zibpay tables
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_resource;" 2>/dev/null')
res_tables = stdout.read().decode('utf-8', errors='ignore').strip()
zibpay_tables = [t for t in res_tables.split('\n') if 'zibpay' in t.lower()]
print('Zibpay tables in wp_resource:', zibpay_tables)

# Check wp_skillxm for zibpay tables
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_skillxm;" 2>/dev/null')
skill_tables = stdout.read().decode('utf-8', errors='ignore').strip()
zibpay_tables2 = [t for t in skill_tables.split('\n') if 'zibpay' in t.lower()]
print('Zibpay tables in wp_skillxm:', zibpay_tables2)

# Check current active theme
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT option_value FROM wp_skillxm.wp_options WHERE option_name = \'template\';"')
print('Current theme:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('[DONE]')