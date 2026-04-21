import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] wp_resource database')

# Check wp_resource posts
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT COUNT(*) FROM wp_resource.wp_posts;"')
print('wp_resource posts:', stdout.read().decode('utf-8', errors='ignore').strip())

# Look for large SQL files
stdin, stdout, stderr = client.exec_command('find /tmp /root -name "*.sql" -size +1M 2>/dev/null')
print('SQL files:', stdout.read().decode('utf-8', errors='ignore').strip())

# Try to export wp_resource tables
print('\n[EXPORT] Trying to export wp_resource to wp_skillxm')
stdin, stdout, stderr = client.exec_command('mysqldump -u root wp_resource | mysql -u root wp_skillxm 2>&1 | head -20')
print('Import result:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

client.close()