import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# First revert nginx to the working resource_site config
cmds = [
    # Revert nginx config to the one that was working
    "ln -sf /etc/nginx/sites-available/resource_site.conf /etc/nginx/sites-enabled/resource_site.conf",
    "rm -f /etc/nginx/sites-enabled/skillxm.cn.conf",
    "nginx -t 2>&1",
    "systemctl reload nginx 2>&1",
    "echo 'nginx reloaded'",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)

import time
time.sleep(2)

# Check if site works now
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=9' 2>/dev/null | wc -c")
print("Page size: " + stdout.read().decode().strip(), flush=True)

# Find the footer.php in the active theme
stdin, stdout, stderr = ssh.exec_command("find /www/wwwroot/resource_site/wp-content/themes/ -name 'footer.php' 2>/dev/null")
footers = stdout.read().decode('utf-8', errors='replace').strip()
print("Footer files: " + footers, flush=True)

# Add sitemap link to footer.php - read it first
stdin, stdout, stderr = ssh.exec_command("tail -20 /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php 2>/dev/null || echo 'footer-not-found'")
print("Footer content:\n" + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

ssh.close()
