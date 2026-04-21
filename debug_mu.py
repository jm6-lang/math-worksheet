import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check mu-plugins
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/wwwroot/resource_site/wp-content/mu-plugins/ 2>&1",
    timeout=5
)
print("mu-plugins:\n%s" % stdout.read().decode().strip())

# Disable all mu-plugins
stdin, stdout, stderr = ssh.exec_command(
    "mkdir -p /www/wwwroot/resource_site/wp-content/mu-plugins-disabled 2>/dev/null; mv /www/wwwroot/resource_site/wp-content/mu-plugins/*.php /www/wwwroot/resource_site/wp-content/mu-plugins-disabled/ 2>/dev/null; echo moved",
    timeout=5
)
print("Disabled mu-plugins: %s" % stdout.read().decode().strip())

import time
time.sleep(2)

# Test
stdin, stdout, stderr = ssh.exec_command(
    "curl -s -D- https://www.skillxm.cn/ 2>/dev/null | head -10",
    timeout=10
)
output = stdout.read().decode('utf-8', errors='ignore')
print("Site:\n%s" % output[:600])

# If still broken, check theme functions.php for syntax error
stdin, stdout, stderr = ssh.exec_command(
    "php -l /www/wwwroot/resource_site/wp-content/themes/yymarket/functions.php 2>&1",
    timeout=5
)
print("\nTheme syntax: %s" % stdout.read().decode().strip())

ssh.close()
