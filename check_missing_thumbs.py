import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check how many posts have thumbnails vs total posts
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT COUNT(*) FROM wp_posts WHERE post_type='post' AND post_status='publish'\" --allow-root",
    timeout=15
)
print("Total published posts:", stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT COUNT(DISTINCT post_id) FROM wp_postmeta WHERE meta_key='_thumbnail_id'\" --allow-root",
    timeout=15
)
print("Posts with thumbnail:", stdout.read().decode().strip())

# Get posts without thumbnails
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID NOT IN (SELECT post_id FROM wp_postmeta WHERE meta_key='_thumbnail_id') LIMIT 10\" --allow-root",
    timeout=15
)
print("\nPosts without thumbnails (first 10):")
print(stdout.read().decode().strip())

# Get available attachment IDs
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='attachment' ORDER BY ID DESC LIMIT 20\" --allow-root",
    timeout=15
)
print("\nAvailable attachments (last 20):")
result = stdout.read().decode().strip()
print(result)

ssh.close()