import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Create minimal WP test
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/test_wp.php', 'w') as f:
    f.write('''<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
echo "Starting WP load...\\n";
$_SERVER['HTTP_HOST'] = 'www.skillxm.cn';
$_SERVER['REQUEST_URI'] = '/';
require_once './wp-load.php';
echo "WP loaded OK\\n";
echo "Home URL: " . home_url() . "\\n";
''')
sftp.close()

stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && php test_wp.php 2>&1",
    timeout=20
)
output = stdout.read().decode('utf-8', errors='ignore')
err = stderr.read().decode('utf-8', errors='ignore')
print("WP Load test:\n%s" % (output + err)[:2000])

ssh.close()
