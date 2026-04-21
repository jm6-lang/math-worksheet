import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Granting wp_user full access to wp_skillxm')

# Grant all privileges
stdin, stdout, stderr = client.exec_command("mysql -u root -e 'GRANT ALL PRIVILEGES ON wp_skillxm.* TO wp_user@localhost;'")
print('Privileges granted:', stdout.read().decode('utf-8', errors='ignore').strip())

stdin, stdout, stderr = client.exec_command('mysql -u root -e "FLUSH PRIVILEGES;"')
print('Flushed')

# Test access to wp_skillxm
stdin, stdout, stderr = client.exec_command('mysql -u wp_user -pgMshA29CshK5 -e "SHOW TABLES FROM wp_skillxm;" 2>&1 | head -5')
print('Tables:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('[DONE]')