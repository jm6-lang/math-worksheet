import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Test the page
stdin, stdout, stderr = ssh.exec_command(
    "curl -sk 'https://skillxm.cn' 2>&1 | grep -o 'login-btn[^>]*data-toggle[^>]*>' | head -2",
    timeout=30
)
print('Login buttons with data-toggle:', stdout.read().decode('utf-8', errors='replace').strip())

# Check for modal
stdin, stdout, stderr = ssh.exec_command(
    "curl -sk 'https://skillxm.cn' 2>&1 | grep -c 'login-modal'",
    timeout=30
)
print('login-modal count:', stdout.read().decode('utf-8', errors='replace').strip())

# Check for bootstrap.js
stdin, stdout, stderr = ssh.exec_command(
    "curl -sk 'https://skillxm.cn' 2>&1 | grep -c 'bootstrap.*\\.js'",
    timeout=30
)
print('Bootstrap JS:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()