import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Finding correct database')

# List all databases
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW DATABASES;"')
dbs = stdout.read().decode('utf-8', errors='ignore').strip()
print('Databases:', dbs)

# Try wp_skillxm database which we saw earlier
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_skillxm;"')
print('wp_skillxm tables:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check wp_skillxm for theme options
stdin, stdout, stderr = client.exec_command("mysql -u root wp_skillxm -e 'SELECT option_name, option_value FROM wp_options WHERE option_name LIKE \"template%\";'")
print('Template settings:', stdout.read().decode('utf-8', errors='ignore').strip())

# Also check siteurl/home
stdin, stdout, stderr = client.exec_command("mysql -u root wp_skillxm -e 'SELECT option_name, option_value FROM wp_options WHERE option_name IN (\"siteurl\", \"home\");'")
print('Site URLs:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()