import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Theme options in DB')

# Search for zibll options
stdin, stdout, stderr = client.exec_command("mysql -u root wp_skillxm -e 'SELECT option_name FROM wp_options WHERE option_name LIKE \"%zibll%\" LIMIT 20;'")
print('Zibll options:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check theme_mod settings
stdin, stdout, stderr = client.exec_command("mysql -u root wp_skillxm -e 'SELECT option_name FROM wp_options WHERE option_name LIKE \"%theme_mod%\";'")
print('Theme mods:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()