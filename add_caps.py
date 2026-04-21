import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[ADD] Admin capabilities')

# Get user ID
stdin, stdout, stderr = client.exec_command('mysql -u root -N -e "SELECT ID FROM wp_skillxm.wp_users WHERE user_login = admin;"')
user_id = stdout.read().decode('utf-8', errors='ignore').strip()
print('User ID:', user_id)

if user_id:
    # Create SQL file for capabilities
    sql = f"USE wp_skillxm;\n"
    sql += f"INSERT IGNORE INTO wp_usermeta (user_id, meta_key, meta_value) VALUES ({user_id}, 'wp_capabilities', 'a:1:{{s:13:\"administrator\";b:1;}}');\n"
    sql += f"INSERT IGNORE INTO wp_usermeta (user_id, meta_key, meta_value) VALUES ({user_id}, 'wp_user_level', '10');\n"
    
    sftp = client.open_sftp()
    f = sftp.file('/tmp/add_caps.sql', 'w')
    f.write(sql)
    f.close()
    
    stdin, stdout, stderr = client.exec_command('mysql -u root < /tmp/add_caps.sql 2>&1')
    print('Capabilities added')

client.close()
print('[DONE]')
print('Login at: https://skillxm.cn/wp-admin')
print('User: admin')
print('Pass: Admin123456')