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

# Look at line 8440 in detail
print('=== admin-options.php line 8438-8442 ===')
out = run_cmd(client, "sed -n '8438,8442p' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php 2>&1")
print(out)

# Look for eval() calls around line 8440
print('\n=== eval() near 8440 ===')
out = run_cmd(client, "sed -n '8430,8450p' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php 2>&1")
print(out[:1000])

# The Parse error might be from code.php or other obfuscated files
# Let me check: is code.php being loaded? code.php was modified before (syntax error fix)
# Check if code.php is being loaded
print('\n=== Is code.php loaded? ===')
out = run_cmd(client, "grep -rn 'code/code\\.php\\|code\\\\/code' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' 2>&1 | grep -v 'Binary\\|\\.disabled' | head -10")
print(out[:500])

# Check if require.php (original) loaded code.php
# The original require.php might have included code.php via its obfuscated code
# Since we replaced require.php with a stub, code.php is NOT loaded
# But maybe other files load code.php?

# Check what loaded the code that causes parse error
# The error says line 8440 has unexpected ')'
# Let me look more carefully at what's on that line
print('\n=== Line 8440 hex dump ===')
out = run_cmd(client, "sed -n '8440p' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php 2>&1 | od -c | head -5")
print(out[:500])

# Actually, the parse error is at RUNTIME from eval'd code, not from admin-options.php itself
# The error message says "in .../admin-options.php on line 8440" which means eval()'d code
# is being executed in the context of admin-options.php
# 
# The real question: what is the actual error? Let me get the full error message
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -o "Parse error[^<]*" | head -1')
print(f'\nFull error: {out}')

# Actually - let me check if this is a CODE.PHP issue
# Previously we modified code.php to fix syntax. Let me check its current state
print('\n=== code.php syntax ===')
out = run_cmd(client, 'php -l /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php 2>&1')
print(out)

# Check code.php against backup
print('\n=== code.php vs backup ===')
out = run_cmd(client, "md5sum /tmp/themes_backup/inc/code/code.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php 2>&1")
print(out)

client.close()