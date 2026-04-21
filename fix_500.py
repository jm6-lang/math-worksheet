import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check advanced-cache.php
cmd = "ls -la /www/wwwroot/resource_site/wp-content/advanced-cache.php 2>/dev/null && head -5 /www/wwwroot/resource_site/wp-content/advanced-cache.php 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("advanced-cache.php:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

# Remove it temporarily
cmd = "mv /www/wwwroot/resource_site/wp-content/advanced-cache.php /www/wwwroot/resource_site/wp-content/advanced-cache.php.bak 2>/dev/null && echo 'moved'"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Result: %s" % stdout.read().decode().strip())

# Remove WP_CACHE define
cmd = "grep -n 'WP_CACHE' /www/wwwroot/resource_site/wp-config.php 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
lines = stdout.read().decode().strip()
print("WP_CACHE lines:\n%s" % lines)

# Test
cmd = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Site: %s" % stdout.read().decode().strip())

ssh.close()