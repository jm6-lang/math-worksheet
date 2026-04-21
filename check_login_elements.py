import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Save page and check for login elements
stdin, stdout, stderr = ssh.exec_command(
    "curl -s -H 'Host: skillxm.cn' http://127.0.0.1 > /tmp/pg.html && wc -c /tmp/pg.html && grep -c 'login-modal' /tmp/pg.html && grep -c 'login-btn' /tmp/pg.html && grep -c 'xenice_login' /tmp/pg.html",
    timeout=60
)
print('Result:', stdout.read().decode('utf-8', errors='replace').strip())

# Check for Bootstrap modal
stdin, stdout, stderr = ssh.exec_command(
    "grep -c 'modal' /tmp/pg.html",
    timeout=10
)
print('Modal count:', stdout.read().decode('utf-8', errors='replace').strip())

# Check for jQuery
stdin, stdout, stderr = ssh.exec_command(
    "grep -c 'jquery' /tmp/pg.html",
    timeout=10
)
print('jQuery count:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()