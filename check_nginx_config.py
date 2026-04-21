import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# List nginx configs
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/server/panel/vhost/nginx/",
    timeout=10
)
print('Nginx configs:', stdout.read().decode('utf-8', errors='replace').strip())

# Check active config
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /etc/nginx/sites-enabled/",
    timeout=10
)
print('Sites enabled:', stdout.read().decode('utf-8', errors='replace').strip())

# Read the active config
stdin, stdout, stderr = ssh.exec_command(
    "cat /etc/nginx/sites-enabled/resource_site.conf 2>/dev/null || cat /etc/nginx/sites-enabled/default",
    timeout=10
)
print('Active config:\n', stdout.read().decode('utf-8', errors='replace'))

ssh.close()