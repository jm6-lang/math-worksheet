import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check WP Super Cache config
cmd = "cat /www/wwwroot/resource_site/wp-content/wp-cache-config.php 2>/dev/null | grep -i 'cache_enabled\\|WPCACHEHOME' | head -5"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("WPSC config:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

# Check if cache config file exists
cmd = "ls -la /www/wwwroot/resource_site/wp-content/wp-cache-config.php 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("Config file: %s" % stdout.read().decode().strip())

# Check wp_options for cache settings
cmd = "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_value FROM wp_options WHERE option_name='ossdl_off_cdn_url' LIMIT 1;\" 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("OSSDL: %s" % stdout.read().decode().strip())

# The issue might be advanced-cache.php referencing a wrong path
# Let me check the content
cmd = "cat /www/wwwroot/resource_site/wp-content/advanced-cache.php 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("\nadvanced-cache.php:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
