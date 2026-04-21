import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Creating and executing SQL file')

# Create SQL file
sql = "USE wp_skillxm;\n"
sql += "INSERT IGNORE INTO wp_options (option_name, option_value) VALUES ('users_can_register', '1');\n"
sql += "INSERT IGNORE INTO wp_options (option_name, option_value) VALUES ('default_role', 'subscriber');\n"

sftp = client.open_sftp()
f = sftp.file('/tmp/enable_reg.sql', 'w')
f.write(sql)
f.close()

# Execute SQL
stdin, stdout, stderr = client.exec_command('mysql -u root < /tmp/enable_reg.sql 2>&1')
print('SQL result:', stdout.read().decode('utf-8', errors='ignore').strip())

# Verify
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT option_name, option_value FROM wp_skillxm.wp_options WHERE option_name = \\"users_can_register\\";"')
print('Check:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('[DONE]')