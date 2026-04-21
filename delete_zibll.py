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

# Step 1: Get DB info and query theme settings
script = r"""
DB_NAME=$(grep "DB_NAME" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_NAME', '\(.*\)'.*/\1/")
DB_USER=$(grep "DB_USER" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_USER', '\(.*\)'.*/\1/")
DB_PASS=$(grep "DB_PASSWORD" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_PASSWORD', '\(.*\)'.*/\1/")
DB_HOST=$(grep "DB_HOST" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_HOST', '\(.*\)'.*/\1/")
echo "DB: DB_NAME=$DB_NAME DB_USER=$DB_USER DB_HOST=$DB_HOST"
mysql -u"$DB_USER" -p"$DB_PASS" -h"$DB_HOST" "$DB_NAME" -e "SELECT option_name, option_value FROM wp_options WHERE option_name IN ('template', 'stylesheet', 'current_theme');" 2>/dev/null
"""

out = run_cmd(client, script)
print('=== Current theme in DB ===')
print(out)

# Step 2: Switch to twentytwentyfour
switch_script = r"""
DB_NAME=$(grep "DB_NAME" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_NAME', '\(.*\)'.*/\1/")
DB_USER=$(grep "DB_USER" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_USER', '\(.*\)'.*/\1/")
DB_PASS=$(grep "DB_PASSWORD" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_PASSWORD', '\(.*\)'.*/\1/")
DB_HOST=$(grep "DB_HOST" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_HOST', '\(.*\)'.*/\1/")

# Switch theme to twentytwentyfour
mysql -u"$DB_USER" -p"$DB_PASS" -h"$DB_HOST" "$DB_NAME" -e "
UPDATE wp_options SET option_value = 'twentytwentyfour' WHERE option_name IN ('template', 'stylesheet');
UPDATE wp_options SET option_value = 'Twenty Twenty-Four' WHERE option_name = 'current_theme';
" 2>/dev/null

echo "Theme switched to twentytwentyfour"

# Verify
mysql -u"$DB_USER" -p"$DB_PASS" -h"$DB_HOST" "$DB_NAME" -e "SELECT option_name, option_value FROM wp_options WHERE option_name IN ('template', 'stylesheet', 'current_theme');" 2>/dev/null
"""

out = run_cmd(client, switch_script)
print('\n=== Switch theme ===')
print(out)

# Step 3: Delete zibll theme (move to backup first)
print('\n=== Deleting zibll theme ===')
out = run_cmd(client, 'mkdir -p /tmp/zibll_backup_deleted && mv /www/wwwroot/resource_site/wp-content/themes/zibll /tmp/zibll_backup_deleted/zibll_$(date +%Y%m%d_%H%M%S) && echo "Moved to /tmp/zibll_backup_deleted/" && ls /tmp/zibll_backup_deleted/')
print(out)

# Verify
out = run_cmd(client, 'ls -1 /www/wwwroot/resource_site/wp-content/themes/')
print(f'\nRemaining themes: {out}')

# Step 4: Restart PHP and test
run_cmd(client, 'systemctl restart php8.1-fpm')
time.sleep(2)

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'\nFrontend after deletion: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -o "<title>[^<]*</title>" | head -1')
print(f'Title: {out}')

# Clean up /etc/hosts zibll entries
out = run_cmd(client, "sed -i '/zibll/d' /etc/hosts && echo 'Cleaned /etc/hosts'")
print(out)

client.close()
