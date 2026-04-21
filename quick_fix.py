import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check PHP-FPM status
stdin, stdout, stderr = ssh.exec_command("systemctl status php8.1-fpm | head -5", timeout=10)
print("PHP-FPM:", stdout.read().decode().strip())

# Check if it failed
stdin, stdout, stderr = ssh.exec_command("systemctl is-failed php8.1-fpm", timeout=5)
failed = stdout.read().decode().strip()
print("Failed:", failed)

# Restart PHP-FPM
stdin, stdout, stderr = ssh.exec_command("systemctl restart php8.1-fpm && echo 'Restarted'", timeout=15)
print("Restart:", stdout.read().decode().strip())

# Test site
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' https://skillxm.cn/", timeout=15)
print("Site:", stdout.read().decode().strip())

ssh.close()
print("Done!")
