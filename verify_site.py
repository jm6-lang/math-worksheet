import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Test site with proper HTTPS
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' -H 'Host: skillxm.cn' https://127.0.0.1/", timeout=15)
print("Site status:", stdout.read().decode().strip())

# Check page content
stdin, stdout, stderr = ssh.exec_command("curl -s -H 'Host: skillxm.cn' https://127.0.0.1/ | head -20", timeout=15)
content = stdout.read().decode().strip()
print("Page size:", len(content), "chars")
print("Content preview:", content[:300])

ssh.close()