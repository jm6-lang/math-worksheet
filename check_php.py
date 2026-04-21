import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check PHP-FPM socket
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /var/run/php/",
    timeout=10
)
print('PHP sockets:', stdout.read().decode('utf-8', errors='replace').strip())

# Check correct socket name
stdin, stdout, stderr = ssh.exec_command(
    "grep 'listen' /etc/php/8.1/fpm/pool.d/www.conf | grep -v '^;'",
    timeout=10
)
print('PHP-FPM listen:', stdout.read().decode('utf-8', errors='replace').strip())

# Test PHP directly
stdin, stdout, stderr = ssh.exec_command(
    "php -r 'echo \"PHP is working\n\";'",
    timeout=10
)
print('PHP test:', stdout.read().decode('utf-8', errors='replace').strip())

# Check if index.php exists
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/wwwroot/resource_site/index.php",
    timeout=10
)
print('Index.php:', stdout.read().decode('utf-8', errors='replace').strip())

# Try accessing index.php directly
stdin, stdout, stderr = ssh.exec_command(
    "curl -s http://localhost/index.php 2>&1 | head -5",
    timeout=30
)
print('Index.php output:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()