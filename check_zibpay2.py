import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Zibpay tables')

# Check available backups
stdin, stdout, stderr = client.exec_command('ls -la /tmp/*.sql /tmp/*backup* 2>/dev/null')
print('Backups:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check wp_resource
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_resource;"')
tables = stdout.read().decode('utf-8', errors='ignore').strip()
print('wp_resource tables:')
for line in tables.split('\n'):
    if 'zibpay' in line.lower():
        print(f'  FOUND: {line}')

# Check total tables
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT COUNT(*) FROM wp_resource.wp_posts;"')
print('wp_resource posts count:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()