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

# Check current hosts file
print('=== /etc/hosts ===')
out = run_cmd(client, 'cat /etc/hosts 2>&1')
print(out)

# Check what domains the obfuscated code connects to
# Use strace on PHP CLI with a very short timeout
print('\n=== DNS connections from PHP ===')
# Test: run PHP loading the theme with strace to see network calls
out = run_cmd(client, 'cd /www/wwwroot/resource_site && timeout 3 strace -f -e trace=connect php -r "echo 1;" 2>&1 | grep connect | head -5', timeout=8)
print(f'strace basic: {out[:500]}')

# Now let's add ALL zibll domains to hosts
print('\n=== Adding all zibll domains to hosts ===')
domains = [
    'zibll.com',
    'www.zibll.com', 
    'api.zibll.com',
    'update.zibll.com',
    'auth.zibll.com',
    'cdn.zibll.com',
    'download.zibll.com',
]

# First check what's already there
out = run_cmd(client, 'cat /etc/hosts 2>&1')
existing_lines = [l for l in out.split('\n') if 'zibll' in l.lower()]
print(f'Existing zibll entries: {existing_lines}')

# Remove existing zibll entries and add new ones
for line in existing_lines:
    run_cmd(client, f"sed -i '/{line.strip()}/d' /etc/hosts")

# Add all domains
hosts_entry = '127.0.0.1 ' + ' '.join(domains)
run_cmd(client, f'echo "{hosts_entry}" >> /etc/hosts')

out = run_cmd(client, 'cat /etc/hosts 2>&1')
print(f'\nUpdated hosts:\n{out}')

# Flush DNS cache
run_cmd(client, 'systemd-resolve --flush-caches 2>/dev/null; resolvectl flush-caches 2>/dev/null; echo done')

# Test
run_cmd(client, 'systemctl restart php8.1-fpm')
time.sleep(2)

print('\n=== Site test with all zibll domains blocked ===')
out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'Frontend: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -o "<title>[^<]*</title>" | head -1')
print(f'Title: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | head -2')
print(f'Page start: {out[:300]}')

client.close()