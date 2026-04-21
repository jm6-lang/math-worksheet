import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check the actual HTML output for a post
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp post list --post_type=post --posts_per_page=1 --fields=ID --format=ids --allow-root",
    timeout=15
)
post_id = stdout.read().decode().strip().split()[0]
print(f"Checking post ID: {post_id}")

# Get thumbnail URL for this post
stdin, stdout, stderr = ssh.exec_command(
    f"cd /www/wwwroot/resource_site && wp post meta get {post_id} _thumbnail_id --allow-root",
    timeout=15
)
thumb_id = stdout.read().decode().strip()
print(f"Thumbnail ID: {thumb_id}")

if thumb_id and thumb_id != '':
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && wp post get {thumb_id} --field=guid --allow-root",
        timeout=15
    )
    thumb_url = stdout.read().decode().strip()
    print(f"Thumbnail URL: {thumb_url}")

# Check if the file actually exists
stdin, stdout, stderr = ssh.exec_command(
    f"ls -la /www/wwwroot/resource_site/wp-content/uploads/2026/04/ | grep -i '{thumb_id}' | head -5",
    timeout=10
)
print(f"\nFiles matching thumbnail ID:")
print(stdout.read().decode().strip())

# Check index.php current state
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '50,60p' /www/wwwroot/resource_site/wp-content/themes/yymarket/index.php",
    timeout=10
)
print(f"\nindex.php lines 50-60:")
print(stdout.read().decode().strip())

ssh.close()