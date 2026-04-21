import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Rebuild wp-super-cache
cmds = [
    # Create cache dir structure
    "mkdir -p /www/wwwroot/resource_site/wp-content/cache/wp-super-cache/skillxm.cn/",
    "chown -R www-data:www-data /www/wwwroot/resource_site/wp-content/cache/",
    
    # Restart PHP-FPM to clear opcode cache
    "systemctl restart php8.1-fpm 2>&1",
    
    # Restart nginx
    "systemctl restart nginx 2>&1",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)

import time
time.sleep(3)

# Test
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=17' 2>/dev/null | wc -c")
print("Page size: " + stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=17' 2>/dev/null | head -c 200")
print("Start: " + stdout.read().decode('utf-8', errors='replace').strip())

# Check nginx error log
stdin, stdout, stderr = ssh.exec_command("tail -10 /var/log/nginx/error.log 2>/dev/null")
print("Nginx error: " + stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
