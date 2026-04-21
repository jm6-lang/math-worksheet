import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Test PHP directly via CLI
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && php index.php 2>&1 | head -20",
    timeout=30
)
print('PHP CLI output:\n', stdout.read().decode('utf-8', errors='replace'))

# Check for PHP errors
stdin, stdout, stderr = ssh.exec_command(
    "tail -20 /var/log/php8.1-fpm/error.log 2>/dev/null || echo 'no log'",
    timeout=10
)
print('PHP-FPM error log:', stdout.read().decode('utf-8', errors='replace'))

ssh.close()