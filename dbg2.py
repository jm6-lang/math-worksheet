import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[DEBUG] Database table structure')

# Show all tables in wp_resource
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_resource;"')
tables = stdout.read().decode('utf-8', errors='ignore').strip()
print('Tables:', tables)

# Check for options table with different name
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_resource;" | grep -i option')
opts = stdout.read().decode('utf-8', errors='ignore').strip()
print('Options-like tables:', opts)

# Try to query using table name directly (maybe prefix is different)
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT * FROM wp_resource.wp_options LIMIT 1;" 2>&1')
result = stdout.read().decode('utf-8', errors='ignore').strip()
print('Query result:', result[:200])

client.close()