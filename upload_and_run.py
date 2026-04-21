import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Upload file via SFTP
sftp = ssh.open_sftp()
sftp.put('C:\\tmp\\img_fetch_v2.py', '/www/wwwroot/resource_site/img_fetch_v2.py')
sftp.close()

print("File uploaded")

# Run it
print("\nRunning...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 img_fetch_v2.py 2>&1",
    timeout=300
)

output = stdout.read().decode('utf-8', errors='replace')
errors = stderr.read().decode('utf-8', errors='replace')

print(output)
if errors:
    print("Errors:", errors[:500])

ssh.close()