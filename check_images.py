import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check media library count
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT COUNT(*) FROM wp_posts WHERE post_type='attachment'\" --allow-root",
    timeout=15
)
print("Media library count:", stdout.read().decode().strip())

# Check posts with thumbnail
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT COUNT(*) FROM wp_postmeta WHERE meta_key='_thumbnail_id' AND meta_value > 0\" --allow-root",
    timeout=15
)
print("Posts with thumbnail:", stdout.read().decode().strip())

# Check a specific post thumbnail
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp post meta get 1 _thumbnail_id --allow-root 2>&1 || echo 'No thumbnail'",
    timeout=15
)
print("Post 1 thumbnail ID:", stdout.read().decode().strip())

# Check uploads directory
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/wwwroot/resource_site/wp-content/uploads/2026/04/ 2>&1 | head -20",
    timeout=10
)
print("\nUploads directory:")
print(stdout.read().decode())

# Check if image files exist
stdin, stdout, stderr = ssh.exec_command(
    "find /www/wwwroot/resource_site/wp-content/uploads -name '*.jpg' -o -name '*.png' 2>/dev/null | wc -l",
    timeout=10
)
print("Image files count:", stdout.read().decode().strip())

ssh.close()