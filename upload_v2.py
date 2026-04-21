import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

sftp = client.open_sftp()
sftp.put(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\custom_style_v2.css',
         '/www/wwwroot/resource_site/wp-content/themes/puock/assets/custom.css')
sftp.close()
print('CSS v2 uploaded')

# Verify the file is there
stdin, stdout, stderr = client.exec_command(
    'ls -la /www/wwwroot/resource_site/wp-content/themes/puock/assets/custom.css',
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace'))

# Clear any opcode cache if exists
stdin, stdout, stderr = client.exec_command(
    'cd /www/wwwroot/resource_site/wp-content/themes/puock/assets && ls -lh custom.css',
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
print('All done!')
