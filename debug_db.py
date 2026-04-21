import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[DEBUG] Checking database directly')

# List all options
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_resource;"')
print('Tables:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check options table structure
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT * FROM wp_resource.wp_options LIMIT 5;"')
print('Options sample:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

client.close()
print('[DONE]')