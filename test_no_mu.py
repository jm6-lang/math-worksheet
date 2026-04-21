import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Disable mu-plugin
ssh.exec_command("mv /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php.off 2>/dev/null", timeout=5)

# Check if the issue is mu-plugins dir being empty - WordPress might complain
cmd = "ls /www/wwwroot/resource_site/wp-content/mu-plugins/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("mu-plugins: %s" % stdout.read().decode().strip() or "(empty)")

# If empty, create a dummy to avoid issues
ssh.exec_command("echo '<?php // placeholder' > /www/wwwroot/resource_site/wp-content/mu-plugins/.keep.php 2>/dev/null", timeout=5)

# Run PHP CLI directly
cmd = "cd /www/wwwroot/resource_site && php index.php 2>&1 | tail -5"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
output = stdout.read().decode('utf-8', errors='ignore')
print("PHP CLI: %s" % output[:500])

ssh.close()
