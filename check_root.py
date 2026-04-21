import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    "ls -la /www/wwwroot/resource_site/wp-config.php 2>/dev/null || echo 'no-wp-here'",
    "ls -la /www/wwwroot/resource_site/index.php 2>/dev/null | head -3",
    "ls /www/wwwroot/resource_site/ 2>/dev/null | head -20",
    "readlink -f /www/wwwroot/resource_site 2>/dev/null",
    "cat /etc/nginx/sites-available/skillxm.cn.conf 2>/dev/null",
    "cat /etc/nginx/sites-available/resource_site.conf 2>/dev/null",
]
for c in cmds:
    print(">> " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    print(flush=True)

ssh.close()
