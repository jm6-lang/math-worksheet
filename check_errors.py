import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check nginx error log
stdin, stdout, stderr = ssh.exec_command("tail -30 /var/log/nginx/error.log", timeout=10)
print("Nginx error log:")
print(stdout.read().decode())

# Check PHP-FPM error log
stdin, stdout, stderr = ssh.exec_command("tail -20 /var/log/php8.1-fpm/error.log", timeout=10)
print("\nPHP-FPM error log:")
print(stdout.read().decode())

# Check PHP-FPM config for slowlog
stdin, stdout, stderr = ssh.exec_command("grep -i slow /etc/php/8.1/fpm/php-fpm.conf", timeout=10)
print("\nPHP-FPM slowlog config:")
print(stdout.read().decode())

# Check www.conf
stdin, stdout, stderr = ssh.exec_command("grep -i slow /etc/php/8.1/fpm/pool.d/www.conf", timeout=10)
print("\nwww.conf slowlog:")
print(stdout.read().decode())

ssh.close()