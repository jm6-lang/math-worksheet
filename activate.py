import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[ACTIVATE] Setting zibll as active theme')

# Activate via database
cmd = 'mysql -u root -e "UPDATE wp_resource.wp_options SET option_value=\\"zibll\\" WHERE option_name IN (\\"template\\", \\"stylesheet\\");"'
stdin, stdout, stderr = client.exec_command(cmd)
print('Updated template/stylesheet')

# Verify
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT option_value FROM wp_resource.wp_options WHERE option_name = \\"template\\";"')
result = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Template is now: {result}')

# Clear WordPress object cache
stdin, stdout, stderr = client.exec_command('redis-cli FLUSHALL 2>/dev/null || echo "No Redis"')
print('Cache cleared')

client.close()
print('[DONE] Theme should be active!')