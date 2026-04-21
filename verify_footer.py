import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Check homepage source for footer content
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/ 2>/dev/null | grep -o 'sitemap_index.xml[^>]*>' | head -3")
out = stdout.read().decode('utf-8', errors='replace').strip()
print("Homepage sitemap ref: " + (out if out else "checking..."))

stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/ 2>/dev/null | grep -o '站点地图[^<]*' | head -3")
out = stdout.read().decode('utf-8', errors='replace').strip()
print("Footer text: " + (out if out else "checking..."))

# Check an article
stdin, stdout, stderr = ssh.exec_command("curl -s 'https://skillxm.cn/?p=800' 2>/dev/null | grep -o 'canonical[^>]*>' | head -2")
out = stdout.read().decode('utf-8', errors='replace').strip()
print("Canonical tag: " + (out if out else "checking..."))

stdin, stdout, stderr = ssh.exec_command("curl -s 'https://skillxm.cn/?p=800' 2>/dev/null | grep 'ld+json' | head -2")
out = stdout.read().decode('utf-8', errors='replace').strip()
print("JSON-LD: " + (out if out else "not found"))

ssh.close()
