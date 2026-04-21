import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

sftp = ssh.open_sftp()

# Read wp-config and add WPCACHEHOME
with sftp.open('/www/wwwroot/resource_site/wp-config.php', 'r') as f:
    config = f.read().decode('utf-8')

# Add WPCACHEHOME before WP_CACHE
wp_cache_line = "define('WP_CACHE', true);"
wpcachehome_line = "define('WPCACHEHOME', '/www/wwwroot/resource_site/wp-content/plugins/wp-super-cache/');"

if 'WPCACHEHOME' not in config:
    config = config.replace(wp_cache_line, wpcachehome_line + "\n" + wp_cache_line)
    print("Added WPCACHEHOME")
else:
    print("WPCACHEHOME already exists")

# Turn off display_errors for production
config = config.replace("define( 'WP_DEBUG_DISPLAY', true );", "define( 'WP_DEBUG_DISPLAY', false );")
config = config.replace("define( 'WP_DEBUG', true );", "define( 'WP_DEBUG', true );")

with sftp.open('/www/wwwroot/resource_site/wp-config.php', 'w') as f:
    f.write(config)
sftp.close()

# Restore mu-plugin
ssh.exec_command("mv /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php.disabled /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php 2>/dev/null; echo restored", timeout=5)

# Test
import time
time.sleep(2)
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null", timeout=10)
print("Site: %s" % stdout.read().decode().strip())

ssh.close()
