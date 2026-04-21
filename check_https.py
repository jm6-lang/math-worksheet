import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# The issue is probably redirect from 80 to 443. Use -L and --insecure
stdin, stdout, stderr = ssh.exec_command(
    "curl -sLk -H 'Host: skillxm.cn' https://127.0.0.1/ -o /tmp/pg2.html && wc -c /tmp/pg2.html && grep -c 'login-btn' /tmp/pg2.html && grep -c 'login-modal' /tmp/pg2.html && grep -c 'xenice' /tmp/pg2.html",
    timeout=60
)
print('HTTPS Result:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
