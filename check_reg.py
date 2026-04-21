import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Registration settings')

# Check error log
stdin, stdout, stderr = client.exec_command('tail -50 /var/log/nginx/error.log 2>/dev/null | tail -20')
print('Recent errors:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check registration settings
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "SELECT option_name, option_value FROM wp_options WHERE option_name = users_can_register;"')
print('Users can register:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check WordPress general settings
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "SELECT option_name, option_value FROM wp_options WHERE option_name LIKE \"%registration%\";"')
print('All registration settings:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()