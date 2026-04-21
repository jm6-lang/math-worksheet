import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Get the full nginx config
stdin, stdout, stderr = ssh.exec_command("cat /etc/nginx/sites-available/skillxm.cn.conf")
config = stdout.read().decode('utf-8', errors='replace')
print("FULL NGINX CONFIG:")
print(config)

# Also check the fastcgi-php.conf snippet
stdin, stdout, stderr = ssh.exec_command("cat /etc/nginx/snippets/fastcgi-php.conf 2>/dev/null")
snippet = stdout.read().decode('utf-8', errors='replace')
print("\nFASTCGI SNIPPET:")
print(snippet)

# Check PHP-FPM socket
stdin, stdout, stderr = ssh.exec_command("ls -la /run/php/php8.1-fpm.sock 2>/dev/null || echo 'socket-not-found'")
print("PHP socket: " + stdout.read().decode('utf-8', errors='replace').strip())

stdin, stdout, stderr = ssh.exec_command("php-fpm8.1 -t 2>&1 || php8.1 -v 2>&1 | head -1")
print("PHP check: " + stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
