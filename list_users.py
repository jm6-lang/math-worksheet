import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] All users in database')

# List all users
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT ID, user_login, user_email FROM wp_skillxm.wp_users;"')
print('Users:', stdout.read().decode('utf-8', errors='ignore').strip())

# Also check user count
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT COUNT(*) FROM wp_skillxm.wp_users;"')
print('User count:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()