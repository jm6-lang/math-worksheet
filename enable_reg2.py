import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Enable registration via direct insert')

# Insert options that don't exist
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "INSERT IGNORE INTO wp_options (option_name, option_value) VALUES (\"users_can_register\", \"1\");"')
print('Inserted users_can_register')

stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "INSERT IGNORE INTO wp_options (option_name, option_value) VALUES (\"default_role\", \"subscriber\");"')
print('Inserted default_role')

# Verify
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "SELECT option_name, option_value FROM wp_options WHERE option_name IN (\"users_can_register\", \"default_role\");"')
print('Settings:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('[DONE]')