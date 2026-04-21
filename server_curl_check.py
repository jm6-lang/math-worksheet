import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Curl from server
stdin, stdout, stderr = ssh.exec_command(
    "curl -s http://localhost | grep -o 'login-modal\\|login-btn\\|xenice_login' | head -10",
    timeout=30
)
print('Page contains:', stdout.read().decode('utf-8', errors='replace').strip())

# Check if footer function is running
stdin, stdout, stderr = ssh.exec_command(
    "curl -s http://localhost | tail -100 | grep -o 'login\\|modal' | head -10",
    timeout=30
)
print('Footer contains:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()