import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Since it's nginx, we need to find the server config
cmds = [
    # Find all nginx configs
    "grep -rl 'skillxm' /etc/nginx/ 2>/dev/null | head -10",
    "grep -rl 'skillxm' /www/server/nginx/ 2>/dev/null | head -10",
    "cat /etc/nginx/sites-enabled/default 2>/dev/null | head -30 || echo 'no-default'",
    "nginx -T 2>/dev/null | grep -B2 -A20 'skillxm' | head -50",
    "ls /etc/nginx/conf.d/ 2>/dev/null",
    "ls /etc/nginx/sites-enabled/ 2>/dev/null",
    "ls /www/server/nginx/conf/ 2>/dev/null | head -10",
    "cat /www/server/nginx/conf/nginx.conf 2>/dev/null | grep -i 'include' | head -10",
]
for c in cmds:
    print(">> " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    print(flush=True)

ssh.close()
