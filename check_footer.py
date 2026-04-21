import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Footer and theme options')

# Search for footer options
stdin, stdout, stderr = client.exec_command("mysql -u root wp_skillxm -e 'SELECT option_name, option_value FROM wp_options WHERE option_name LIKE \"%footer%\" OR option_name LIKE \"%copyright%\";'")
print('Footer options:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check theme options folder
stdin, stdout, stderr = client.exec_command('ls -la /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/')
print('Options folder:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

client.close()