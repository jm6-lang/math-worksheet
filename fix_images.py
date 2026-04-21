import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check file details
upload_dir = '/www/wwwroot/resource_site/wp-content/uploads/2026/04/'

stdin, stdout, stderr = ssh.exec_command(
    f"file {upload_dir}category_*.png",
    timeout=10
)
print("File types:")
print(stdout.read().decode())

# Check if files are valid images
stdin, stdout, stderr = ssh.exec_command(
    f"ls -la {upload_dir}category_*.png",
    timeout=10
)
print("File details:")
print(stdout.read().decode())

# Try to fix permissions
stdin, stdout, stderr = ssh.exec_command(
    f"chown www-data:www-data {upload_dir}category_*.png && chmod 644 {upload_dir}category_*.png",
    timeout=10
)
print("Fixed permissions")

# Try importing with force
stdin, stdout, stderr = ssh.exec_command(
    f"cd /www/wwwroot/resource_site && wp media import {upload_dir}category_novel.png --title='小说资源' --porcelain --allow-root 2>&1",
    timeout=15
)
result = stdout.read().decode()
print(f"\nImport result: {result}")

ssh.close()