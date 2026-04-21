import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Write a debug PHP script and serve it via the web
php_debug = '''<?php
// Quick debug
$_GET['test'] = '1';
foreach ($_GET as $k => $v) { $$k = $v; }
define('ABSPATH', '/www/wwwroot/skillxm.cn/public/');
require_once '/www/wwwroot/skillxm.cn/public/wp-load.php';
echo "Template: " . get_template_directory() . "\\n";
echo "Template URI: " . get_template_directory_uri() . "\\n";
echo "Stylesheet: " . get_stylesheet_directory() . "\\n";
echo "Stylesheet URI: " . get_stylesheet_directory_uri() . "\\n";
echo "Current theme: " . wp_get_theme()->get_stylesheet() . "\\n";
'''.encode('utf-8')

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\debug.php', 'wb') as f:
    f.write(php_debug)

sftp = client.open_sftp()
sftp.put(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\debug.php',
         '/www/wwwroot/skillxm.cn/public/debug.php')
sftp.close()
print('Debug file uploaded')

# Fetch it
import time; time.sleep(1)
stdin, stdout, stderr = client.exec_command(
    'curl -s "http://127.0.0.1/debug.php" 2>&1',
    timeout=15
)
print('Debug output:')
print(stdout.read().decode('utf-8', errors='replace'))

# Clean up
stdin, stdout, stderr = client.exec_command(
    'rm /www/wwwroot/skillxm.cn/public/debug.php',
    timeout=5
)
print('Cleaned up')

client.close()
