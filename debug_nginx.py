import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Check nginx status
    "systemctl status nginx 2>/dev/null | head -5",
    
    # Check what config is active
    "ls -la /etc/nginx/sites-enabled/",
    
    # Test locally
    "curl -sI http://127.0.0.1/ -H 'Host: skillxm.cn' 2>/dev/null | head -5",
    
    # Check if the new config is actually loaded
    "nginx -T 2>/dev/null | grep 'root ' | head -5",
    
    # Test with verbose
    "curl -v https://skillxm.cn/ 2>&1 | head -20",
    
    # Check SSL
    "openssl s_client -connect skillxm.cn:443 -servername skillxm.cn </dev/null 2>/dev/null | head -10",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    print(flush=True)

ssh.close()
