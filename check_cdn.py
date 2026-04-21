import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Check DNS for CDN
    "dig skillxm.cn +short 2>/dev/null || nslookup skillxm.cn 2>/dev/null | grep Address | tail -2",
    
    # Check if local curl works with IP directly
    "curl -s 'http://127.0.0.1/' -H 'Host: skillxm.cn' 2>/dev/null | wc -c",
    
    # Check if there's a CDN header from outside
    "curl -sI https://skillxm.cn/ 2>/dev/null | grep -iE 'x-cache|cf-|cdn|su-|proxy|via|ali'",
    
    # Check nginx access log for the latest request
    "tail -5 /var/log/nginx/access.log 2>/dev/null || tail -5 /var/log/nginx/skillxm_access.log 2>/dev/null || echo 'no-log'",
    
    # Find nginx log files
    "find /var/log/nginx/ -name '*skillxm*' -o -name '*access*' 2>/dev/null | head -5",
    
    # Check if there's a CDN/security plugin
    "wp plugin list --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null | grep -iE 'cdn|cloud|security|cache'",
    
    # Full page from local
    "curl -s 'http://127.0.0.1/' -H 'Host: skillxm.cn' 2>/dev/null | head -30",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    print(flush=True)

ssh.close()
