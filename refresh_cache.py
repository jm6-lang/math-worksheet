import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Change ver=1.0 to ver=2.0 to bust cache
stdin, stdout, stderr = client.exec_command(
    "sed -i 's/ver=1.0/ver=2.0/g' /www/wwwroot/resource_site/wp-content/themes/puock/functions.php",
    timeout=10
)
stdout.read()
print('Updated version to 2.0')

# Verify
stdin, stdout, stderr = client.exec_command(
    'grep -n "sk-custom" /www/wwwroot/resource_site/wp-content/themes/puock/functions.php',
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
