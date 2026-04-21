import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Get the latest attachment IDs (the ones we just uploaded)
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID, post_title FROM wp_posts WHERE post_type='attachment' ORDER BY ID DESC LIMIT 10\" --allow-root",
    timeout=15
)
print("Latest attachments:")
print(stdout.read().decode())

# Check if files exist
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/wwwroot/resource_site/wp-content/uploads/2026/04/category_*.png",
    timeout=10
)
print("\nCategory files:")
print(stdout.read().decode())

ssh.close()