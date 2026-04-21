# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

commands = [
    # Create mu-plugins dir
    "mkdir -p /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins",
    
    # Check nginx config for sitemap rewrite
    "cat /www/server/panel/vhost/nginx/skillxm.cn.conf 2>/dev/null | head -50 || cat /etc/nginx/sites-enabled/skillxm.cn 2>/dev/null | head -50 || echo 'nginx-conf-not-found'",
    
    # Check what generated the robots.txt (plugin or file)
    "ls -la /www/wwwroot/skillxm.cn/public/robots.txt 2>/dev/null",
    
    # Check if virtual robots exists (Yoast generates virtual)
    "curl -s https://skillxm.cn/robots.txt 2>/dev/null | wc -l",
    
    # Check nginx rewrite rules
    "grep -r 'rewrite' /www/server/panel/vhost/nginx/skillxm.cn.conf 2>/dev/null | head -20 || echo 'no-rewrite'",
]

for cmd in commands:
    print(">> {}".format(cmd), flush=True)
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    print(flush=True)

ssh.close()
