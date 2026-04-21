import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Upload CSS to correct path
sftp = client.open_sftp()
sftp.put(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\custom_style_v2.css',
         '/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/css/custom-style.css')
sftp.close()
print('CSS uploaded to correct path!')

# Bump version to 1.0.1 to force refresh
stdin, stdout, stderr = client.exec_command(
    "sed -i \"s/'1.0.0');/'1.0.1');/\" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php",
    timeout=10
)
stdout.read()

# Verify
stdin, stdout, stderr = client.exec_command(
    'grep -n "custom-style.css\\|1.0.1" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php | grep -v "^#\|^//"',
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace'))

# Verify file exists
stdin, stdout, stderr = client.exec_command(
    'ls -lh /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/css/custom-style.css',
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
print('All done!')
