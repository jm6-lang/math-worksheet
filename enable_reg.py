import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[ENABLE] User registration in WordPress')

# Enable registration
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "UPDATE wp_options SET option_value = 1 WHERE option_name = users_can_register;"')
print('Update result:', stdout.read().decode('utf-8', errors='ignore').strip())

# Also set default role
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "UPDATE wp_options SET option_value = subscriber WHERE option_name = default_role;"')
print('Default role set')

# Verify
stdin, stdout, stderr = client.exec_command("mysql -u root wp_skillxm -e 'SELECT option_value FROM wp_options WHERE option_name = users_can_register;'")
print('Registration status:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('[DONE] Registration enabled!')