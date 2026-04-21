import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Get the skillxm_custom_styles function body
stdin, stdout, stderr = client.exec_command(
    'sed -n "761,770p" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php',
    timeout=10
)
print('skillxm_custom_styles function:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
