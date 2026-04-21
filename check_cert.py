import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check SSL certificate files
stdin, stdout, stderr = ssh.exec_command("ls -la /etc/letsencrypt/live/skillxm.cn/", timeout=10)
print("SSL certificate files:")
print(stdout.read().decode())

# Test SSL connection locally
stdin, stdout, stderr = ssh.exec_command("openssl s_client -connect 127.0.0.1:443 -servername skillxm.cn 2>&1 | head -20", timeout=15)
print("\nSSL test:")
print(stdout.read().decode())

ssh.close()