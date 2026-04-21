import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Test HTTPS
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' -H 'Host: skillxm.cn' https://127.0.0.1/", timeout=15)
print("HTTPS status:", stdout.read().decode().strip())

# Test with www
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' -H 'Host: www.skillxm.cn' https://127.0.0.1/", timeout=15)
print("www HTTPS status:", stdout.read().decode().strip())

# Get page title
stdin, stdout, stderr = ssh.exec_command("curl -sL -H 'Host: skillxm.cn' https://127.0.0.1/ | grep -o '<title>[^<]*</title>'", timeout=15)
print("Page title:", stdout.read().decode().strip())

ssh.close()
print("\nDone!")
