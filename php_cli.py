import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Run PHP directly to see error
cmd = "cd /www/wwwroot/resource_site && php -d display_errors=On index.php 2>&1 | head -50"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
print("PHP CLI output:\n%s" % stdout.read().decode('utf-8', errors='ignore')[:2500])

# Also check if wp-settings.php exists
cmd = "ls -la /www/wwwroot/resource_site/wp-settings.php 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("\nwp-settings.php: %s" % stdout.read().decode().strip())

# Check for syntax errors
cmd = "php -l /www/wwwroot/resource_site/wp-config.php 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("PHP lint: %s" % stdout.read().decode().strip())

# Check debug log
cmd = "tail -30 /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
log = stdout.read().decode('utf-8', errors='ignore')
print("\nDebug log:\n%s" % log[-2000:] if log else "(empty)")

ssh.close()
