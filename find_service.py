import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Find what process manager is running
stdin, stdout, stderr = client.exec_command(
    'ps aux 2>/dev/null | grep -E "php-fpm|php|nginx" | head -10',
    timeout=10
)
print('Running processes:')
print(stdout.read().decode('utf-8', errors='replace'))

# Check systemctl
stdin, stdout, stderr = client.exec_command(
    'which systemctl service init.d 2>/dev/null; ls /etc/init.d/ 2>/dev/null | head -10',
    timeout=10
)
print('Init system:')
print(stdout.read().decode('utf-8', errors='replace'))

# Check what service is listening on port 80
stdin, stdout, stderr = client.exec_command(
    'ss -tlnp 2>/dev/null | grep -E ":80|:443" || netstat -tlnp 2>/dev/null | grep -E ":80|:443"',
    timeout=10
)
print('Port 80 listeners:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
