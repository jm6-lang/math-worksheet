import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check nginx SSL config
stdin, stdout, stderr = ssh.exec_command("cat /etc/nginx/sites-enabled/resource_site.conf", timeout=10)
print("Nginx SSL config:")
print(stdout.read().decode())

# Check if SSL is properly configured
stdin, stdout, stderr = ssh.exec_command("grep -i 'ssl_certificate\\|listen.*ssl' /etc/nginx/sites-enabled/resource_site.conf", timeout=10)
print("\nSSL directives:")
print(stdout.read().decode())

# Test nginx -t
stdin, stdout, stderr = ssh.exec_command("nginx -t 2>&1", timeout=10)
print("\nNginx test:")
print(stdout.read().decode())

ssh.close()