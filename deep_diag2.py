import paramiko, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

def run_cmd(cmd, timeout=10):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

# Write the test PHP script to server via SFTP (avoids shell injection issues)
test_php = """<?php
$_SERVER["HTTP_HOST"] = "skillxm.cn";
$_SERVER["REQUEST_URI"] = "/";
$_SERVER["HTTPS"] = "on";
$_SERVER["DOCUMENT_ROOT"] = "/www/wwwroot/resource_site";
define("ABSPATH", "/www/wwwroot/resource_site/");
require_once ABSPATH . "wp-load.php";
echo "WP_OK\\n";
flush();
// Now load the theme
require "/www/wwwroot/resource_site/wp-content/themes/zibll/functions.php";
echo "THEME_OK\\n";
"""

sftp = client.open_sftp()
with sftp.file('/tmp/test_theme.php', 'w') as f:
    f.write(test_php)
sftp.close()

print('=== Test: Load WP + Zibll theme with 5s timeout ===')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_theme.php 2>&1', timeout=15)
print(out[:2000])

# Nginx error log
print('\n=== Nginx error log (last 10) ===')
out = run_cmd('tail -10 /www/wwwlogs/skillxm.cn.error.log 2>&1')
print(out[:1000])

# Response headers
print('\n=== Response headers ===')
out = run_cmd('curl -s -k -D - --max-time 5 -o /dev/null https://127.0.0.1/ 2>&1')
print(out[:500])

# PHP-FPM status
print('\n=== PHP-FPM status ===')
out = run_cmd('systemctl is-active php8.1-fpm 2>&1')
print(out)

# Also check: what happens when we request with curl but trace what PHP does
# Use a simple PHP info page to verify PHP-FPM works
print('\n=== PHP info test ===')
sftp = client.open_sftp()
with sftp.file('/www/wwwroot/resource_site/info.php', 'w') as f:
    f.write('<?php phpinfo(); ?>')
sftp.close()
out = run_cmd('curl -s -k --max-time 5 https://127.0.0.1/info.php 2>&1 | head -5')
print(out[:300])
run_cmd('rm /www/wwwroot/resource_site/info.php')

client.close()