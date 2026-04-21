import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Restore wp-config.php WP_CACHE
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/wp-config.php', 'r') as f:
    config = f.read().decode('utf-8')

# Uncomment WP_CACHE
config = config.replace("// define('WP_CACHE', true);", "define('WP_CACHE', true);")

# Check for WPCACHEHOME which was a known issue
if 'WPCACHEHOME' in config:
    print("WARNING: WPCACHEHOME found - removing")
    lines = config.split('\n')
    new_lines = [l for l in lines if 'WPCACHEHOME' not in l]
    config = '\n'.join(new_lines)

with sftp.open('/www/wwwroot/resource_site/wp-config.php', 'w') as f:
    f.write(config)
sftp.close()
print("wp-config.php restored")

# Restore advanced-cache.php
ssh.exec_command("mv /www/wwwroot/resource_site/wp-content/advanced-cache.php.off /www/wwwroot/resource_site/wp-content/advanced-cache.php 2>/dev/null; echo done", timeout=5)

# Check actual PHP error via curl with verbose output
import time
time.sleep(2)
stdin, stdout, stderr = ssh.exec_command("curl -s -D- https://www.skillxm.cn/ 2>/dev/null | head -40", timeout=15)
output = stdout.read().decode('utf-8', errors='ignore')
print("\nCurl output:\n%s" % output[:2000])

ssh.close()
