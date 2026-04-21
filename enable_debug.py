import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[ENABLE] WordPress debug mode')

# Read wp-config
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-config.php', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

# Enable debug
content = content.replace("define( 'WP_DEBUG', false );", "define( 'WP_DEBUG', true );")
content = content.replace("define( 'WP_DEBUG', false );", "define( 'WP_DEBUG', true );")

# Write back
f = sftp.file('/www/wwwroot/resource_site/wp-config.php', 'w')
f.write(content)
f.close()

print('WP_DEBUG enabled')

# Test again
stdin, stdout, stderr = client.exec_command('curl -s http://127.0.0.1/ 2>&1 | head -100')
print('Error details:', stdout.read().decode('utf-8', errors='ignore').strip()[:1000])

client.close()