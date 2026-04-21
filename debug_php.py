import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Create a simple test.php
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/test_debug.php', 'w') as f:
    f.write('<?php echo "PHP OK"; phpinfo(); ?>')
sftp.close()

stdin, stdout, stderr = ssh.exec_command(
    "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/test_debug.php 2>/dev/null",
    timeout=10
)
code = stdout.read().decode().strip()
print("test.php: %s" % code)

if code == '200':
    stdin, stdout, stderr = ssh.exec_command(
        "curl -s https://www.skillxm.cn/test_debug.php 2>/dev/null | head -5",
        timeout=10
    )
    print("Output: %s" % stdout.read().decode()[:200])

# Check PHP-FPM pool config
stdin, stdout, stderr = ssh.exec_command(
    "cat /etc/php/8.1/fpm/pool.d/www.conf | grep -E 'php_admin_value|catch_workers|pm' | head -10",
    timeout=10
)
print("\nPool config:\n%s" % stdout.read().decode().strip())

# Check if there's a custom PHP error handler in the theme
stdin, stdout, stderr = ssh.exec_command(
    "grep -r 'wp_die\\|die(\\|exit(' /www/wwwroot/resource_site/wp-content/themes/yymarket/functions.php 2>/dev/null | head -10",
    timeout=10
)
print("\nTheme die/exit:\n%s" % stdout.read().decode().strip())

# Test with direct PHP-FPM
stdin, stdout, stderr = ssh.exec_command(
    "SCRIPT_NAME=/test_debug.php SCRIPT_FILENAME=/www/wwwroot/resource_site/test_debug.php REQUEST_METHOD=GET cgi-fcgi -bind -connect /run/php/php8.1-fpm.sock 2>&1 | head -10",
    timeout=10
)
print("\nDirect FCGI:\n%s" % stdout.read().decode('utf-8', errors='ignore')[:500])

ssh.close()
