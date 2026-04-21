import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Order class for CREATE TABLE')

# Read order-class.php
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/class/order-class.php', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

# Find create_db function
in_create = False
for i, line in enumerate(content.split('\n'), 1):
    if 'create_db' in line.lower() or in_create:
        print(f'Line {i}: {line.strip()[:150]}')
        in_create = True
        if in_create and ('}' in line and 'function' not in line):
            in_create = False

client.close()