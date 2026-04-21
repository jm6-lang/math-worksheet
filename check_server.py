import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')
cmds = [
    "which apache2 && echo 'apache' || echo 'no-apache'",
    "which nginx && echo 'nginx' || echo 'no-nginx'",
    "systemctl list-units --type=service --state=running | grep -E 'apache|nginx|httpd'",
    "ps aux | grep -E 'apache|nginx|httpd' | grep -v grep | head -5",
    "cat /www/wwwroot/skillxm.cn/public/.htaccess 2>/dev/null || echo 'no-htaccess'",
    "curl -sI https://skillxm.cn/ 2>/dev/null | head -10",
    "curl -s https://skillxm.cn/sitemap_index.xml 2>/dev/null | head -10",
]
for c in cmds:
    print(">> " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    print(flush=True)
ssh.close()
