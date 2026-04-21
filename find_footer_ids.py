import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[BEAUTIFY] Set footer with correct Zibll keys')

# Read admin-options.php more to find exact key names for footer content area
stdin, stdout, stderr = client.exec_command("grep -n \"'id'.*footer\" /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php | head -40")
print('Footer option IDs:', stdout.read().decode('utf-8', errors='ignore').strip()[:1500])

client.close()