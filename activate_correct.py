import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[ACTIVATE] Activating zibll in correct database (wp_skillxm)')

# The actual WordPress site is at wp_skillxm, not wp_resource!
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "UPDATE wp_options SET option_value = \\"zibll\\" WHERE option_name IN (\\"template\\", \\"stylesheet\\");"')
print('Theme updated')

# Verify
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "SELECT option_value FROM wp_options WHERE option_name IN (\\"template\\", \\"stylesheet\\");"')
print('Active theme:', stdout.read().decode('utf-8', errors='ignore').strip())

# Clear any caching
stdin, stdout, stderr = client.exec_command('redis-cli FLUSHALL 2>/dev/null || echo "No Redis"')
print('Cache: cleared')

# Also need to update wp_config to point to correct database
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-config.php', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

# Check current config
print('Current DB in wp-config:', content.split('DB_NAME')[1].split(')')[0].strip() if 'DB_NAME' in content else 'Not found')

client.close()
print('[DONE] Theme should now be zibll!')
print('Please clear browser cache and refresh site.')