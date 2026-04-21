import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[ADD] Admin capabilities for user ID 3')

# User ID is 3 for admin
user_id = 3

# Create SQL to add capabilities
sql = f"""USE wp_skillxm;
INSERT IGNORE INTO wp_usermeta (user_id, meta_key, meta_value) VALUES ({user_id}, 'wp_capabilities', 'a:1:{{s:13:"administrator";b:1;}}');
INSERT IGNORE INTO wp_usermeta (user_id, meta_key, meta_value) VALUES ({user_id}, 'wp_user_level', '10');
"""

sftp = client.open_sftp()
f = sftp.file('/tmp/add_caps3.sql', 'w')
f.write(sql)
f.close()

# Execute
stdin, stdout, stderr = client.exec_command('mysql -u root < /tmp/add_caps3.sql 2>&1')
print('Result:', stdout.read().decode('utf-8', errors='ignore').strip())

# Verify
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT meta_value FROM wp_skillxm.wp_usermeta WHERE user_id = 3 AND meta_key = wp_capabilities;"')
print('Capabilities:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('[DONE]')
print('Login at: https://skillxm.cn/wp-admin')
print('User: admin')
print('Pass: Admin123456')