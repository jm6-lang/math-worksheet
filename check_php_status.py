import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check PHP-FPM status
stdin, stdout, stderr = ssh.exec_command("systemctl status php8.1-fpm | head -10", timeout=10)
print("PHP-FPM status:")
print(stdout.read().decode())

# Check if PHP-FPM is running
stdin, stdout, stderr = ssh.exec_command("ps aux | grep php-fpm | grep -v grep | head -3", timeout=10)
print("\nPHP-FPM processes:")
print(stdout.read().decode())

# Check socket
stdin, stdout, stderr = ssh.exec_command("ls -la /run/php/", timeout=10)
print("\nPHP socket:")
print(stdout.read().decode())

# Test PHP directly
stdin, stdout, stderr = ssh.exec_command("php -r 'echo \"PHP OK\\n\";'", timeout=10)
print("\nPHP CLI test:")
print(stdout.read().decode())

# Test via curl to localhost:80 (no SSL)
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost | head -5", timeout=15)
print("\nSite via HTTP:")
print(stdout.read().decode()[:200])

ssh.close()