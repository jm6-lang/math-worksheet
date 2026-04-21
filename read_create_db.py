import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[READ] order-class.php create_db full function')

sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/class/order-class.php', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

# Print lines 30 to 120
lines = content.split('\n')
for i in range(29, min(120, len(lines))):
    print(f'{i+1}: {lines[i]}')

client.close()