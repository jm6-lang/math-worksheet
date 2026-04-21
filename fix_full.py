import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# List available themes
cmd = "cd /www/wwwroot/resource_site && wp theme list --allow-root 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("Themes:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

# Check error log more carefully
cmd = "tail -30 /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
log = stdout.read().decode('utf-8', errors='ignore')
# Filter only errors, not notices
for line in log.split('\n'):
    if 'Fatal' in line or 'Error' in line or 'error' in line.lower():
        print("ERR: %s" % line[:200])

# Disable all plugins except core
print("\nDisabling all plugins...")
cmd = "cd /www/wwwroot/resource_site && wp plugin deactivate --all --allow-root 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("%s" % stdout.read().decode().strip())

# Test
cmd = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Site: %s" % stdout.read().decode().strip())

ssh.close()