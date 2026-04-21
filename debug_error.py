import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check PHP error log
cmd = "tail -30 /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
log = stdout.read().decode('utf-8', errors='ignore')
if log:
    print("debug.log:\n%s" % log[-2000:])
else:
    print("No debug.log")

# Check PHP-FPM log
cmd = "tail -20 /var/log/php8.1-fpm.log 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
log = stdout.read().decode('utf-8', errors='ignore')
if log:
    print("php-fpm.log:\n%s" % log[-1000:])

# Try accessing the site directly
cmd = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Site HTTP: %s" % stdout.read().decode().strip())

# Disable mu-plugin temporarily to check
cmd = "mv /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php.bak 2>/dev/null && echo disabled"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Mu-plugin: %s" % stdout.read().decode().strip())

# Check if site works now
import time
time.sleep(1)
cmd = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/?p=1812 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Site after disable: %s" % stdout.read().decode().strip())

ssh.close()
