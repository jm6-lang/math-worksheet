import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Use localhost with Host header
stdin, stdout, stderr = ssh.exec_command(
    "curl -s -H 'Host: skillxm.cn' http://127.0.0.1/ -o /tmp/pg.html && wc -c /tmp/pg.html",
    timeout=30
)
print('Size:', stdout.read().decode('utf-8', errors='replace').strip())

# Check for login elements
stdin, stdout, stderr = ssh.exec_command(
    "grep -c 'login-btn\\|login-modal' /tmp/pg.html",
    timeout=10
)
print('Login elements:', stdout.read().decode('utf-8', errors='replace').strip())

# Check for xenice_login
stdin, stdout, stderr = ssh.exec_command(
    "grep -c 'xenice' /tmp/pg.html",
    timeout=10
)
print('Xenice refs:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()