import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Compare themes
    "echo '=== resource_site themes ===' && ls /www/wwwroot/resource_site/wp-content/themes/ 2>/dev/null",
    "echo '=== skillxm themes ===' && ls /www/wwwroot/skillxm.cn/public/wp-content/themes/ 2>/dev/null",
    
    # Check if wp-content is same across both
    "diff <(ls /www/wwwroot/resource_site/wp-content/ 2>/dev/null) <(ls /www/wwwroot/skillxm.cn/public/wp-content/ 2>/dev/null)",
    
    # Try switching back to resource_site config
    "echo '=== Switching back to resource_site ==='",
    "rm -f /etc/nginx/sites-enabled/skillxm.cn.conf",
    "ln -sf /etc/nginx/sites-available/resource_site.conf /etc/nginx/sites-enabled/resource_site.conf",
    "nginx -t 2>&1",
    "systemctl reload nginx 2>&1",
    
    # Check if skillxm.cn/public has a theme with footer customization
    "ls /www/wwwroot/skillxm.cn/public/wp-content/themes/ 2>/dev/null",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    if err: print("ERR: " + err, flush=True)
    print(flush=True)

ssh.close()
