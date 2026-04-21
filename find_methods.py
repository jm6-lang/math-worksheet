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

# Find all ZibAut method calls in the theme
print('=== All ZibAut:: method calls ===')
out = run_cmd(client, "grep -rn 'ZibAut::' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' 2>&1 | grep -v 'Binary\\|\\.disabled' | head -30")
print(out[:2000])

# Also check for zib_is_aut and aut_required calls
print('\n=== zib_is_aut / aut_required calls ===')
out = run_cmd(client, "grep -rn 'zib_is_aut\\|aut_required' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' 2>&1 | grep -v 'Binary\\|function\\|\\.disabled' | head -20")
print(out[:1000])

client.close()