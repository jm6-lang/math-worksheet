import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Read local file
with open(r'C:\Users\Administrator\Desktop\新建文件夹\baidu_verify_codeva-YrdJwkcfZ3.html', 'rb') as f:
    content = f.read()

print(f"Local file size: {len(content)} bytes")

# Upload to server root
sftp = ssh.open_sftp()
remote_path = '/www/wwwroot/resource_site/baidu_verify_codeva-YrdJwkcfZ3.html'
with sftp.open(remote_path, 'wb') as f:
    f.write(content)
sftp.close()

print(f"Uploaded to: {remote_path}")

# Verify
stdin, stdout, stderr = ssh.exec_command(f"ls -la {remote_path}", timeout=10)
print("Server file:", stdout.read().decode().strip())

# Test HTTP access
stdin, stdout, stderr = ssh.exec_command(
    "curl -sI 'https://www.skillxm.cn/baidu_verify_codeva-YrdJwkcfZ3.html' 2>&1 | head -5",
    timeout=15
)
print("\nHTTP check:", stdout.read().decode().strip())

ssh.close()
print("\nDone!")