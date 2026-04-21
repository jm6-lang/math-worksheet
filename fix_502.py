import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check nginx status
stdin, stdout, stderr = ssh.exec_command("systemctl status nginx | head -5", timeout=10)
print("Nginx:", stdout.read().decode().strip())

# Check PHP-FPM status
stdin, stdout, stderr = ssh.exec_command("systemctl status php8.1-fpm | head -5", timeout=10)
print("PHP-FPM:", stdout.read().decode().strip())

# Create slowlog directory
stdin, stdout, stderr = ssh.exec_command("mkdir -p /var/log/php-fpm && touch /var/log/php-fpm/slow.log && chown www-data:www-data /var/log/php-fpm/slow.log", timeout=10)
print("Slowlog created:", stdout.read().decode().strip())

# Restart PHP-FPM
stdin, stdout, stderr = ssh.exec_command("systemctl restart php8.1-fpm && systemctl status php8.1-fpm | head -5", timeout=15)
print("PHP-FPM restart:", stdout.read().decode().strip())

# Check nginx
stdin, stdout, stderr = ssh.exec_command("systemctl reload nginx && echo 'Nginx reloaded'", timeout=10)
print("Nginx:", stdout.read().decode().strip())

# Test site
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' https://skillxm.cn/", timeout=15)
print("Site HTTP status:", stdout.read().decode().strip())

ssh.close()
print("\nDone!")
