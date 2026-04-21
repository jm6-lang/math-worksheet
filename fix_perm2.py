import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Fix permissions again
ssh.exec_command("chown www-data:www-data /www/wwwroot/resource_site/wp-config.php", timeout=10)
ssh.exec_command("chmod 640 /www/wwwroot/resource_site/wp-config.php", timeout=10)
ssh.exec_command("systemctl restart php8.1-fpm", timeout=10)

import time
time.sleep(2)

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=final' 2>/dev/null | wc -c")
print("Page size: " + stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command("tail -5 /var/log/nginx/error.log 2>/dev/null")
print("Nginx error: " + stdout.read().decode('utf-8', errors='replace').strip()[-300:])

ssh.close()
