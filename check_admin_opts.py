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

def run_cmd(client, cmd, timeout=10):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

client = connect()

# Check admin-options.php around line 8440
print('=== admin-options.php line 8435-8445 ===')
out = run_cmd(client, "sed -n '8435,8445p' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php 2>&1")
print(out[:1000])

# Check if we have a backup
print('\n=== Check backup ===')
out = run_cmd(client, 'ls -la /tmp/themes_backup/inc/options/admin-options.php 2>&1')
print(out)

# Compare with backup
out = run_cmd(client, "diff /tmp/themes_backup/inc/options/admin-options.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php 2>&1 | head -20")
print(f'\nDiff: {out[:1000]}')

client.close()