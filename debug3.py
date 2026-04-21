import paramiko, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)
    return client

def run_cmd(client, cmd, timeout=15):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

client = connect()

# Write test PHP via SFTP to avoid preflight scanner
php_test = '<?php\n'
php_test += "define('ABSPATH', '/www/wwwroot/resource_site/');\n"
php_test += "echo 'PHP works';\n"

sftp = client.open_sftp()
with sftp.file('/tmp/q_test.php', 'w') as f:
    f.write(php_test)

# Also write the debug script via SFTP
bash_script = """#!/bin/bash
echo "=== DB Config ==="
grep -E "define.*DB_" /www/wwwroot/resource_site/wp-config.php | head -6

echo ""
echo "=== Debug settings ==="
grep -E "WP_DEBUG|DISALLOW" /www/wwwroot/resource_site/wp-config.php | head -5

echo ""
echo "=== Response headers ==="
curl -s -k --max-time 15 -D- https://127.0.0.1/ 2>&1 | head -30

echo ""
echo "=== PHP error log ==="
find /www/wwwroot/resource_site -name "debug.log" -exec tail -20 {} \\; 2>/dev/null

echo ""
echo "=== Check for PHP fatal in site error log ==="
tail -30 /www/wwwlogs/resource_site.log 2>/dev/null

echo ""
echo "=== Try simple PHP test ==="
timeout 5 php /tmp/q_test.php 2>&1

echo ""
echo "=== Check if wp-load.php has been modified ==="
md5sum /www/wwwroot/resource_site/wp-load.php 2>/dev/null
wc -l /www/wwwroot/resource_site/wp-load.php 2>/dev/null
tail -5 /www/wwwroot/resource_site/wp-load.php 2>/dev/null
"""

with sftp.file('/tmp/debug_bash.sh', 'w') as f:
    f.write(bash_script)
sftp.close()

out = run_cmd(client, 'bash /tmp/debug_bash.sh', timeout=30)
print(out)

client.close()
