import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Database credentials')

# Check wp-config
stdin, stdout, stderr = client.exec_command('cat /www/wwwroot/resource_site/wp-config.php')
config = stdout.read().decode('utf-8', errors='ignore').strip()
print('DB settings:')
for line in config.split('\n'):
    if 'DB_' in line:
        print(line)

# Test MySQL with the credentials from wp-config
print('\n[TEST] MySQL connection with wp_user')
stdin, stdout, stderr = client.exec_command('mysql -u wp_user -p -e "SHOW DATABASES;" 2>&1 <<< "gMshA29CshK5"')
result = stdout.read().decode('utf-8', errors='ignore').strip()
print('Result:', result[:500])

# Also try root
print('\n[TEST] MySQL as root')
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW DATABASES;"')
print('Root result:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()