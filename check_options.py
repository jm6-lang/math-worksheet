import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Options table')

# Check options table structure
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "DESC wp_options;"')
print('Table structure:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Count options
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "SELECT COUNT() FROM wp_options;"')
count = stdout.read().decode('utf-8', errors='ignore').strip()
print('Total options:', count)

# Check if insert worked - look at all options with registration in name
stdin, stdout, stderr = client.exec_command('mysql -u root wp_skillxm -e "SELECT option_id, option_name, option_value FROM wp_options WHERE option_name LIKE %registration%;"'  )
print('Registration options:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()