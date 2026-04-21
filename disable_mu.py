import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Disable mu-plugin to get site working
print("Disabling mu-plugin temporarily...")
cmd = "mv /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php.disabled 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Moved: %s" % stdout.read().decode().strip())

# Clear cache
cmd = "rm -rf /www/wwwroot/resource_site/wp-content/cache/* 2>/dev/null && echo 'cache cleared'"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Cache: %s" % stdout.read().decode().strip())

# Test site
cmd = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Site: %s" % stdout.read().decode().strip())

ssh.close()