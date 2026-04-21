import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Get posts by category and assign appropriate thumbnails
# Categories from earlier: 小说资源, 影视资源, 网赚项目, 教程合集

# Get category IDs
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp term list category --fields=term_id,name --format=csv --allow-root",
    timeout=15
)
cats = stdout.read().decode('utf-8', errors='replace')
print("Categories:")
print(cats)

# Get some attachment IDs to use
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='attachment' ORDER BY ID DESC LIMIT 20\" --allow-root",
    timeout=15
)
attachments = [l.strip() for l in stdout.read().decode().strip().split('\n')[1:] if l.strip()]
print(f"\nAvailable attachments: {len(attachments)}")
print(attachments[:10])

ssh.close()