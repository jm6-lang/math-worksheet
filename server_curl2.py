import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Simple check - save to file
stdin, stdout, stderr = ssh.exec_command(
    "curl -s -o /tmp/page.html http://localhost && grep -c 'login-modal' /tmp/page.html && grep -c 'login-btn' /tmp/page.html && grep -c 'jquery' /tmp/page.html && grep -c 'xenice_login' /tmp/page.html",
    timeout=60
)
result = stdout.read().decode('utf-8', errors='replace').strip()
print('Counts:', result)

err = stderr.read().decode('utf-8', errors='replace').strip()
if err:
    print('Error:', err)

ssh.close()
