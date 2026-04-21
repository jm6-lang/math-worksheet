import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Fixing database password')

# Check current users
stdin, stdout, stderr = client.exec_command("mysql -u root -e 'SELECT user, host FROM mysql.user;'")
print('MySQL users:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

# Reset wp_user password
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"ALTER USER 'wp_user'@'localhost' IDENTIFIED BY 'gMshA29CshK5';\"")
print('Password updated')

# Flush privileges
stdin, stdout, stderr = client.exec_command('mysql -u root -e "FLUSH PRIVILEGES;"')
print('Flush privileges')

# Test connection
stdin, stdout, stderr = client.exec_command("mysql -u wp_user -pgMshA29CshK5 -e 'SHOW DATABASES;' 2>&1")
print('Test result:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('[DONE]')