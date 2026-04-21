import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[UPDATE] Site settings via SQL')

# Create SQL file for site settings
sql = "USE wp_skillxm;\n"
sql += "UPDATE wp_options SET option_value = '极创项目网' WHERE option_name = 'blogname';\n"
sql += "UPDATE wp_options SET option_value = '网创项目资源站-副业项目-创业项目-搞钱项目' WHERE option_name = 'blogdescription';\n"

sftp = client.open_sftp()
f = sftp.file('/tmp/site_settings.sql', 'w')
f.write(sql)
f.close()

# Execute
stdin, stdout, stderr = client.exec_command('mysql -u root < /tmp/site_settings.sql 2>&1')
print('Site settings updated')

# Verify
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT option_name, option_value FROM wp_skillxm.wp_options WHERE option_name IN (\\"blogname\\", \\"blogdescription\\");"')
print('Verify:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()