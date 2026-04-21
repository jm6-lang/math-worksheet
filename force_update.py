import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Check current enqueue in skillxm functions.php
stdin, stdout, stderr = client.exec_command(
    'grep -n "skillxm-custom\\|custom-style.css" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php',
    timeout=10
)
print('Current enqueue:')
print(stdout.read().decode('utf-8', errors='replace'))

# Remove the old skillxm_custom_styles function entirely and replace with direct file update approach
# Instead, let's overwrite the old custom.css in /puock/assets/ with our new CSS
# (this file is what the HTML is actually loading from)
sftp = client.open_sftp()
sftp.put(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\custom_style_v2.css',
         '/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/custom.css')
sftp.close()
print('Overwrote custom.css with new content')

# Update version in skillxm functions.php to match
# Change 1.0.1 to 1.0.2 to force refresh
stdin, stdout, stderr = client.exec_command(
    "sed -i \"s/'1.0.1');/'1.0.2');/\" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php",
    timeout=10
)
stdout.read()
print('Updated version to 1.0.2')

# Verify
stdin, stdout, stderr = client.exec_command(
    'grep -n "custom-style.css\\|1.0.2" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php',
    timeout=10
)
print('After update:')
print(stdout.read().decode('utf-8', errors='replace'))

# Touch functions.php to bust OPcache
stdin, stdout, stderr = client.exec_command(
    'touch /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php && echo "touched"',
    timeout=5
)
stdout.read()

# Also restart php-fpm
stdin, stdout, stderr = client.exec_command(
    'systemctl restart php8.1-fpm 2>&1',
    timeout=15
)
print('PHP-FPM restart:', stdout.read().decode('utf-8', errors='replace'), stderr.read().decode('utf-8', errors='replace'))

# Now check if the HTML has the new version
stdin, stdout, stderr = client.exec_command(
    'curl -s "http://127.0.0.1/" 2>&1 | grep -i "custom-style\\|sk-custom\\|1.0.2" | head -3',
    timeout=15
)
print('New HTML check:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
