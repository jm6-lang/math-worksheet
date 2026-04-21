import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check nginx access log for recent requests
cmd = "tail -10 /www/wwwlogs/resource_site.log 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Access log:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

# Check PHP-FPM status
cmd = "systemctl status php8.1-fpm 2>&1 | head -15"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("\nPHP-FPM status:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

# Check nginx status
cmd = "systemctl status nginx 2>&1 | head -10"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("\nNginx status:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

# Test with PHP directly
cmd = "cd /www/wwwroot/resource_site && php index.php 2>&1 | head -30"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
php_output = stdout.read().decode('utf-8', errors='ignore')
print("\nPHP index.php:\n%s" % php_output[:1500] if php_output else "(empty)")

ssh.close()
