import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Fix ownership on ALL resource_site files
    "chown -R www-data:www-data /www/wwwroot/resource_site/",
    "chmod 644 /www/wwwroot/resource_site/wp-config.php",
    
    # Verify
    "ls -la /www/wwwroot/resource_site/wp-config.php",
    
    # Also check the fastcgi socket - it's using /var/run/php/php-fpm.sock but we saw php8.1-fpm.sock earlier
    "ls -la /var/run/php/ 2>/dev/null | grep sock",
    "ls -la /run/php/ 2>/dev/null | grep sock",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    print(flush=True)

import time
time.sleep(2)

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=18' 2>/dev/null | wc -c")
print("Page size: " + stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=18' 2>/dev/null | head -c 300")
print("Start:\n" + stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
