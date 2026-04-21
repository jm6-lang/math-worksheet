import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Re-enable WP Super Cache
print("Re-enabling WP Super Cache...")
cmd = "cd /www/wwwroot/resource_site && wp plugin activate wp-super-cache --allow-root 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("Activate: %s" % stdout.read().decode().strip())

# Check PHP error
cmd = "tail -10 /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("\nPHP log:\n%s" % stdout.read().decode('utf-8', errors='ignore')[-1000:])

# Test site
cmd = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Site HTTP: %s" % stdout.read().decode().strip())

ssh.close()