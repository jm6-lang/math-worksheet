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

# Search for what includes code/file.php specifically
print('=== What includes code/file.php? ===')
out = run_cmd(client, "grep -rn 'code/file\\|code\\\\/file' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' 2>&1 | grep -v 'Binary\\|\\.disabled' | head -20")
print(out[:1500])

# Check the original require.php - what files does it load?
# The strings output showed ZibToolRequire::init() at line 126
# Let me check if there are require/include statements before that
# Since it's binary/obfuscated, let me use a different approach:
# Run PHP to trace what files get loaded

print('\n=== Trace file includes ===')
trace_b64 = "PD9waHAKJF9TRVJWRVJbIkhUVFBfSE9TVCJdID0gInNraWxseG0uY24iOwokX1NFUlZFUlsiUkVRVUVTVF9VUkkiXSA9ICIvIjsKJF9TRVJWRVJbIkhUVFBTIl0gPSAib24iOwokX1NFUlZFUlsiRE9DVU1FTlRfUk9PVCJdID0gIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlIjsKJF9TRVJWRVJbIlNFUlZFUl9QT1JUIl0gPSAiNDQzIjsKZGVmaW5lKCJBQlNQQVRIIiwgIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlLyIpOwpzZXRfZXJyb3JfaGFuZGxlcihmdW5jdGlvbigkZSwgJG0pIHsKICAgIGVjaG8gIiRtXG4iOwogICAgcmV0dXJuIGZhbHNlOwp9KTsKcmVxdWlyZV9vbmNlIEFCU1BBVEggLiAid3AtbG9hZC5waHAiOwplY2hvICJXUF9PS1xuIjsK"
run_cmd(client, f'echo "{trace_b64}" | base64 -d > /tmp/test_trace.php')

out = run_cmd(client, 'cd /www/wwwroot/resource_site && timeout 10 php -d display_errors=1 /tmp/test_trace.php 2>&1', timeout=15)
# Filter for code/ file references
lines = out.split('\n')
code_lines = [l for l in lines if 'code/' in l and ('.php' in l or 'Fatal' in l)]
print(f'code/ references: {chr(10).join(code_lines[:20])}')

# The simplest fix: just rename file.php so it doesn't conflict
# The original require.php loaded it, but now our stub doesn't need it
# Let's see what file.php provides and if it's needed

# Actually, even better: the stub defines classes that file.php ALSO defines.
# The issue is file.php is loaded by SOME OTHER mechanism.
# Let me check: does the theme's inc.php or any other file include code/file.php?

# Check inc/class/class.php - it loads class files
print('\n=== class.php loads: ===')
out = run_cmd(client, "cat /www/wwwroot/resource_site/wp-content/themes/zibll/inc/class/class.php 2>&1 | head -30")
print(out[:1000])

client.close()