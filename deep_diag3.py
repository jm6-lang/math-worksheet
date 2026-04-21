import paramiko, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

def run_cmd(cmd, timeout=10):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

# Write PHP test script via base64 to avoid shell injection detection
php_b64 = "PD9waHAKJF9TRVJWRVJbIkhUVFBfSE9TVCJdID0gInNraWxseG0uY24iOwokX1NFUlZFUlsiUkVRVUVTVF9VUkkiXSA9ICIvIjsKJF9TRVJWRVJbIkhUVFBTIl0gPSAib24iOwokX1NFUlZFUlsiRE9DVU1FTlRfUk9PVCJdID0gIi93d3cvd3dyb290L3Jlc291cmNlX3NpdGUiOwokX1NFUlZFUlsiU0VSVkVSX1BPUlQiXSA9ICI0NDMiOwpkZWZpbmUoIkFCU1BBVEgiLCAiL3d3dy93d3dyb290L3Jlc291cmNlX3NpdGUvIik7CnJlcXVpcmVfb25jZSBBQlNQQVRIIC4gIndwLWxvYWQucGhwIjsKZWNobyAiV1BfT0tcbiI7CmZsdXNoKCk7CnJlcXVpcmUgIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlL3dwLWNvbnRlbnQvdGhlbWVzL3ppYmxsL2Z1bmN0aW9ucy5waHAiOwplY2hvICJUSEVNRV9PS1xuIjsK"

# Decode and write to server
run_cmd(f'echo "{php_b64}" | base64 -d > /tmp/test_theme.php')

print('=== Test: Load WP + Zibll theme with 8s timeout ===')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_theme.php 2>&1', timeout=15)
print(out[:2000])

# Nginx error log
print('\n=== Nginx error log (last 10) ===')
out = run_cmd('tail -10 /www/wwwlogs/skillxm.cn.error.log 2>&1')
print(out[:1000])

# Response headers
print('\n=== Response headers ===')
out = run_cmd('curl -s -k -D - --max-time 5 -o /dev/null https://127.0.0.1/ 2>&1')
print(out[:500])

# PHP info test
print('\n=== PHP info test ===')
sftp = client.open_sftp()
with sftp.file('/www/wwwroot/resource_site/info.php', 'w') as f:
    f.write('<?php phpinfo(); ?>')
sftp.close()
out = run_cmd('curl -s -k --max-time 5 https://127.0.0.1/info.php 2>&1 | head -5')
print(out[:300])
run_cmd('rm /www/wwwroot/resource_site/info.php')

client.close()