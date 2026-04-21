import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check nginx status
stdin, stdout, stderr = ssh.exec_command(
    "systemctl status nginx | head -5",
    timeout=10
)
print('Nginx:', stdout.read().decode('utf-8', errors='replace').strip())

# Check PHP-FPM status
stdin, stdout, stderr = ssh.exec_command(
    "systemctl status php8.1-fpm | head -5",
    timeout=10
)
print('PHP-FPM:', stdout.read().decode('utf-8', errors='replace').strip())

# Check correct site root
stdin, stdout, stderr = ssh.exec_command(
    "grep -i 'root\\|server_name' /www/server/panel/vhost/nginx/*.conf 2>/dev/null | head -20",
    timeout=10
)
print('Nginx configs:', stdout.read().decode('utf-8', errors='replace').strip())

# Try curl with proper hostname
stdin, stdout, stderr = ssh.exec_command(
    "curl -s -H 'Host: skillxm.cn' http://127.0.0.1 | wc -l",
    timeout=30
)
print('Page lines:', stdout.read().decode('utf-8', errors='replace').strip())

# Check PHP error log
stdin, stdout, stderr = ssh.exec_command(
    "tail -20 /www/wwwlogs/skillxm.cn.error.log 2>/dev/null || tail -20 /var/log/php8.1-fpm/error.log 2>/dev/null || echo 'No error log found'",
    timeout=10
)
print('Errors:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
