import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Show full wp-config.php
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/wp-config.php",
    timeout=10
)
config = stdout.read().decode('utf-8', errors='ignore')
print("=== wp-config.php ===")
print(config)

# Check PHP error by running wp-load.php directly  
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && php -d display_errors=1 -r \"define('WP_USE_THEMES', true); require './wp-load.php';\" 2>&1 | head -30",
    timeout=15
)
err_output = stderr.read().decode('utf-8', errors='ignore')
std_output = stdout.read().decode('utf-8', errors='ignore')
print("\n=== PHP Error ===")
print("stdout: %s" % std_output[:1000])
print("stderr: %s" % err_output[:1000])

ssh.close()
