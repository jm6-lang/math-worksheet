import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Search for the actual login button click event binding
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'login-btn\\|data-toggle\\|modal' /tmp/pg2.html | head -20",
    timeout=10
)
print('Login modal refs:', stdout.read().decode('utf-8', errors='replace'))

# Search for Bootstrap CSS (modal needs it)
stdin, stdout, stderr = ssh.exec_command(
    "grep -c 'bootstrap' /tmp/pg2.html",
    timeout=10
)
print('Bootstrap refs:', stdout.read().decode('utf-8', errors='replace'))

# Check if bootstrap.min.js is loaded
stdin, stdout, stderr = ssh.exec_command(
    "grep 'bootstrap' /tmp/pg2.html | head -5",
    timeout=10
)
print('Bootstrap details:', stdout.read().decode('utf-8', errors='replace'))

# Check for inline script handling login
stdin, stdout, stderr = ssh.exec_command(
    "grep -c 'script.js\\|\\.js' /tmp/pg2.html",
    timeout=10
)
print('JS files:', stdout.read().decode('utf-8', errors='replace'))

# Check the full page for script tags
stdin, stdout, stderr = ssh.exec_command(
    "grep -o '<script[^>]*src=[^>]*>' /tmp/pg2.html | head -20",
    timeout=10
)
print('Script tags:', stdout.read().decode('utf-8', errors='replace'))

ssh.close()
