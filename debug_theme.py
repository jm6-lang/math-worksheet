import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[DEBUG] Checking why theme not changed')

# Check themes directory
stdin, stdout, stderr = client.exec_command('ls -la /www/wwwroot/resource_site/wp-content/themes/')
print('Themes:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check zibll folder size
stdin, stdout, stderr = client.exec_command('du -sh /www/wwwroot/resource_site/wp-content/themes/zibll/')
print('Zibll size:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check database theme settings
stdin, stdout, stderr = client.exec_command("mysql -u root wp_resource -e 'SELECT option_name, option_value FROM wp_options WHERE option_name LIKE \"%template%\" OR option_name LIKE \"%stylesheet%\";'")
print('DB theme:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check what site URL is
stdin, stdout, stderr = client.exec_command("mysql -u root wp_resource -e 'SELECT option_name, option_value FROM wp_options WHERE option_name IN (\"siteurl\", \"home\");'")
print('Site URLs:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check if there's a different database being used
stdin, stdout, stderr = client.exec_command('cat /www/wwwroot/resource_site/wp-config.php | grep DB_NAME')
print('DB Name:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()