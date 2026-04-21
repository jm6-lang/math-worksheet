import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Check if custom.css exists in the correct theme dir
stdin, stdout, stderr = client.exec_command(
    'ls -la /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/',
    timeout=10
)
print('skillxm theme assets:')
print(stdout.read().decode('utf-8', errors='replace'))

# Upload CSS to correct path
sftp = client.open_sftp()
sftp.put(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\custom_style_v2.css',
         '/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/custom.css')
sftp.close()
print('CSS uploaded to skillxm.cn!')

# Check functions.php in correct location
stdin, stdout, stderr = client.exec_command(
    'grep -n "custom.css\\|sk-custom" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php',
    timeout=10
)
content = stdout.read().decode('utf-8', errors='replace').strip()
print('Custom CSS enqueue in skillxm:', content)

client.close()
