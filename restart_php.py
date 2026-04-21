import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Restart php8.1-fpm to clear OPcache
stdin, stdout, stderr = client.exec_command(
    'systemctl restart php8.1-fpm 2>&1',
    timeout=15
)
print('Restart result:')
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out, err)

# Wait a moment then verify
import time; time.sleep(2)

# Now check the HTML output
stdin, stdout, stderr = client.exec_command(
    'curl -s "https://skillxm.cn/" 2>&1 | grep -i "custom" | head -5',
    timeout=15
)
print('New HTML CSS refs:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
