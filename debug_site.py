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

# Check actual page output
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | head -20')
print(f'Page output:\n{out}')

# Check if PHP error
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | tail -20')
print(f'\nPage tail:\n{out}')

# Check PHP error log
out = run_cmd(client, 'tail -20 /www/wwwlogs/resource_site.log 2>/dev/null || tail -20 /var/log/php8.1-fpm.log 2>/dev/null || echo "no log found"')
print(f'\nPHP log:\n{out}')

# Check wp-content has no mu-plugins or dropins that reference zibll
out = run_cmd(client, 'ls -la /www/wwwroot/resource_site/wp-content/mu-plugins/ 2>/dev/null; ls -la /www/wwwroot/resource_site/wp-content/drop-ins/ 2>/dev/null; echo "---"; grep -rl "zibll\\|ZibAut" /www/wwwroot/resource_site/wp-content/plugins/ 2>/dev/null | head -10')
print(f'\nZibll references:\n{out}')

# Check if functions.php still references zibll
out = run_cmd(client, "grep -n 'zibll\\|ZibAut\\|inc/code/require' /www/wwwroot/resource_site/wp-content/themes/twentytwentyfour/functions.php 2>/dev/null || echo 'clean'")
print(f'\nTheme functions.php: {out}')

# Check the current theme is actually twentytwentyfour
script = r"""DB_NAME=$(grep "DB_NAME" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_NAME', '\\''\\(.*\\)'\\''.*/\\1/")
DB_USER=$(grep "DB_USER" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_USER', '\\''\\(.*\\)'\\''.*/\\1/")
DB_PASS=$(grep "DB_PASSWORD" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_PASSWORD', '\\''\\(.*\\)'\\''.*/\\1/")
DB_HOST=$(grep "DB_HOST" /www/wwwroot/resource_site/wp-config.php | head -1 | sed "s/.*DB_HOST', '\\''\\(.*\\)'\\''.*/\\1/")
mysql -u"${DB_USER}" -p"${DB_PASS}" -h"${DB_HOST}" "${DB_NAME}" -N -e "SELECT option_value FROM wp_options WHERE option_name IN ('template','stylesheet');" 2>/dev/null
"""
sftp = client.open_sftp()
with sftp.file('/tmp/check_db.sh', 'w') as f:
    f.write(script)
sftp.close()
out = run_cmd(client, 'bash /tmp/check_db.sh')
print(f'\nDB theme settings: {out}')

client.close()
