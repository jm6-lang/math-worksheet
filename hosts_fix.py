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

# The original require.php is obfuscated. Let me try a different approach:
# Instead of replacing require.php, let's just disable the network calls.
#
# The blocking likely happens because ZibToolRequire::init() tries to connect
# to zibll.com. If we can make that function a no-op while keeping everything else...
#
# But the whole file is obfuscated. We can't easily modify just the init() method.
#
# Alternative: what if we add a hosts file entry to redirect zibll.com to 127.0.0.1?
# This would make the connection fail immediately instead of timing out.

print('=== Strategy: Block zibll.com via hosts file ===')

# First restore original require.php
run_cmd(client, 'cp /tmp/themes_backup/inc/code/require.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/require.php')
print('Restored original require.php')

# Add zibll.com to /etc/hosts pointing to 127.0.0.1
# This will make any connection to zibll.com fail immediately
out = run_cmd(client, "grep zibll /etc/hosts 2>&1")
if 'zibll' not in out:
    run_cmd(client, 'echo "127.0.0.1 zibll.com www.zibll.com" >> /etc/hosts')
    print('Added zibll.com to /etc/hosts')
else:
    print('zibll.com already in hosts')

# Verify
out = run_cmd(client, "grep zibll /etc/hosts 2>&1")
print(f'hosts: {out}')

# Test
run_cmd(client, 'systemctl restart php8.1-fpm')
time.sleep(2)

# Quick test: can PHP resolve zibll.com now?
print('\n=== DNS test ===')
out = run_cmd(client, 'timeout 3 php -r "echo gethostbyname(\"zibll.com\");" 2>&1')
print(f'zibll.com resolves to: {out}')

# Test curl
out = run_cmd(client, 'timeout 3 curl -s -o /dev/null -w "%{http_code}" https://zibll.com 2>&1')
print(f'curl zibll.com: {out}')

# Test the site
print('\n=== Site test ===')
out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'Frontend: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/wp-login.php 2>&1')
print(f'Login: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -o "<title>[^<]*</title>" | head -1')
print(f'Title: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -i "fatal\\|parse error" | head -3')
if out:
    print(f'Errors: {out[:500]}')
else:
    print('No errors!')

client.close()