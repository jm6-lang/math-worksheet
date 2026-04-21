import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Disable ALL plugins temporarily
print("Disabling all plugins via DB...")
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"UPDATE wp_options SET option_value='a:0:{}' WHERE option_name='active_plugins';\" 2>/dev/null && echo done",
    timeout=10
)
print("%s" % stdout.read().decode().strip())

import time
time.sleep(2)

# Clear all caches
stdin, stdout, stderr = ssh.exec_command(
    "rm -rf /www/wwwroot/resource_site/wp-content/cache/* 2>/dev/null && echo cleared",
    timeout=5
)
print("Cache: %s" % stdout.read().decode().strip())

# Test with minimal WP
stdin, stdout, stderr = ssh.exec_command(
    "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null",
    timeout=10
)
code = stdout.read().decode().strip()
print("Site (no plugins): %s" % code)

if code == '200':
    print("\n✓ Site works with no plugins. Re-enabling essential ones...")
    plugins = ['auto-post-thumbnail', 'insert-headers-and-footers', 'wp-super-cache']
    for p in plugins:
        ssh.exec_command(
            "cd /www/wwwroot/resource_site && wp plugin activate %s --allow-root 2>&1" % p,
            timeout=15
        )
    time.sleep(1)
    stdin, stdout, stderr = ssh.exec_command(
        "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null",
        timeout=10
    )
    print("Site (essential plugins): %s" % stdout.read().decode().strip())

ssh.close()
