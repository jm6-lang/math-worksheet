import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Zibpay functions.php for table creation')

# Read zibpay functions.php
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/functions.php', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

# Look for CREATE TABLE
for i, line in enumerate(content.split('\n'), 1):
    if 'CREATE' in line.upper() or 'TABLE' in line.upper() or 'install' in line.lower() or 'activate' in line.lower():
        print(f'Line {i}: {line.strip()[:120]}')

print('\n--- Full functions.php ---')
print(content[:3000])

client.close()