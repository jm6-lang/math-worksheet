import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

sftp = client.open_sftp()
sftp.put(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\custom_style.css',
         '/www/wwwroot/resource_site/wp-content/themes/puock/assets/custom.css')
sftp.close()
print('CSS uploaded')

# Check current theme functions for how styles are enqueued
_, o = client.exec_command(
    'grep -n "wp_enqueue_style\\|wp_enqueue_scripts" /www/wwwroot/resource_site/wp-content/themes/puock/functions.php | head -5',
    timeout=10
)
content = o.read().decode('utf-8', errors='replace').strip()
print('Found enqueue lines:', content)

# Find the right place to add our CSS
_, o = client.exec_command(
    'grep -n "function.*enqueue\\|add_action.*wp_enqueue" /www/wwwroot/resource_site/wp-content/themes/puock/functions.php | head -5',
    timeout=10
)
content2 = o.read().decode('utf-8', errors='replace').strip()
print('Enqueue actions:', content2)

# Get the last few lines of the enqueue function
_, o = client.exec_command(
    'grep -n "wp_enqueue_style" /www/wwwroot/resource_site/wp-content/themes/puock/functions.php | tail -3',
    timeout=10
)
lines = o.read().decode('utf-8', errors='replace').strip()
print('Current enqueue styles:', lines)

client.close()
