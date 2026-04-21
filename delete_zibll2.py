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

# Write the script to remote server first
script = r'''#!/bin/bash
# Get DB credentials
DB_NAME=$(grep "DB_NAME" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_NAME', '\(.*\)'.*/\1/")
DB_USER=$(grep "DB_USER" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_USER', '\(.*\)'.*/\1/")
DB_PASS=$(grep "DB_PASSWORD" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_PASSWORD', '\(.*\)'.*/\1/")
DB_HOST=$(grep "DB_HOST" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_HOST', '\(.*\)'.*/\1/")

echo "=== Current theme ==="
mysql -u"$DB_USER" -p"$DB_PASS" -h"$DB_HOST" "$DB_NAME" -e "SELECT option_name, option_value FROM wp_options WHERE option_name IN ('template', 'stylesheet', 'current_theme');" 2>/dev/null

echo ""
echo "=== Switching to twentytwentyfour ==="
mysql -u"$DB_USER" -p"$DB_PASS" -h"$DB_HOST" "$DB_NAME" -e "
UPDATE wp_options SET option_value = 'twentytwentyfour' WHERE option_name IN ('template', 'stylesheet');
UPDATE wp_options SET option_value = 'Twenty Twenty-Four' WHERE option_name = 'current_theme';
" 2>/dev/null

echo "Switched. Verifying:"
mysql -u"$DB_USER" -p"$DB_PASS" -h"$DB_HOST" "$DB_NAME" -e "SELECT option_name, option_value FROM wp_options WHERE option_name IN ('template', 'stylesheet', 'current_theme');" 2>/dev/null

echo ""
echo "=== Moving zibll theme to backup ==="
mkdir -p /tmp/zibll_backup_deleted
if [ -d /www/wwwroot/resource_site/wp-content/themes/zibll ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    mv /www/wwwroot/resource_site/wp-content/themes/zibll /tmp/zibll_backup_deleted/zibll_$TIMESTAMP
    echo "Moved to /tmp/zibll_backup_deleted/zibll_$TIMESTAMP"
else
    echo "zibll theme not found"
fi

echo ""
echo "=== Remaining themes ==="
ls -1 /www/wwwroot/resource_site/wp-content/themes/

echo ""
echo "=== Cleaning /etc/hosts ==="
sed -i '/zibll/d' /etc/hosts
echo "Cleaned zibll entries from /etc/hosts"
cat /etc/hosts

echo ""
echo "=== Restarting PHP-FPM ==="
systemctl restart php8.1-fpm
sleep 2

echo "=== Testing site ==="
curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/
echo ""
curl -s -k --max-time 15 https://127.0.0.1/ | grep -o "<title>[^<]*</title>" | head -1

echo ""
echo "DONE"
'''

sftp = client.open_sftp()
with sftp.file('/tmp/delete_zibll.sh', 'w') as f:
    f.write(script)
sftp.close()

run_cmd(client, 'chmod +x /tmp/delete_zibll.sh')
out = run_cmd(client, 'bash /tmp/delete_zibll.sh', timeout=30)
print(out)

client.close()
