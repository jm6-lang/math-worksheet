import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check wp-config for issues
cmd = "php -l /www/wwwroot/resource_site/wp-config.php 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("PHP lint: %s" % stdout.read().decode().strip())

# Check if the WPCACHEHOME line is back (it was a known issue before)
cmd = "grep -n 'WPCACHE\\|WP_CACHE\\|advanced-cache' /www/wwwroot/resource_site/wp-config.php"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Cache lines:\n%s" % stdout.read().decode().strip())

# Check recent error log entries
cmd = "tail -5 /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("\nDebug log tail:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

# Restore advanced-cache.php since WP Super Cache might need it
cmd = "mv /www/wwwroot/resource_site/wp-content/advanced-cache.php.bak /www/wwwroot/resource_site/wp-content/advanced-cache.php 2>/dev/null; echo 'restored'"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("advanced-cache: %s" % stdout.read().decode().strip())

# Re-enable critical plugins
print("\nRe-enabling plugins...")
for plugin in ['wp-super-cache', 'auto-post-thumbnail', 'insert-headers-and-footers', 'zhanzhangb-baidu-submit']:
    cmd = "cd /www/wwwroot/resource_site && wp plugin activate %s --allow-root 2>&1" % plugin
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    print("  %s: %s" % (plugin, stdout.read().decode().strip()))

# Test
cmd = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Site: %s" % stdout.read().decode().strip())

ssh.close()