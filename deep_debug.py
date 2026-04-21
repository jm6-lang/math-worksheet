import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check nginx error log for this site
cmd = "tail -20 /www/wwwlogs/resource_site.error.log 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Nginx error log:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

# Try PHP directly
cmd = "php -r \"echo file_get_contents('/www/wwwroot/resource_site/wp-load.php') ? 'ok' : 'fail';\" 2>&1 | tail -3"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("\nPHP test: %s" % stdout.read().decode('utf-8', errors='ignore')[:500])

# Check disk space
cmd = "df -h /www/wwwroot/resource_site 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("\nDisk: %s" % stdout.read().decode().strip())

# Check if wp-config has the old WPCACHEHOME issue  
cmd = "cat /www/wwwroot/resource_site/wp-config.php | grep -n 'WPCACHE\\|require.*wp-settings'"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Config cache lines:\n%s" % stdout.read().decode().strip())

ssh.close()