import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check some posts with thumbnails
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT post_id, meta_value FROM wp_postmeta WHERE meta_key='_thumbnail_id' LIMIT 5\" --allow-root",
    timeout=15
)
print("Sample posts with thumbnails:")
print(stdout.read().decode().strip())

# Check attachment URLs
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID, guid FROM wp_posts WHERE post_type='attachment' LIMIT 5\" --allow-root",
    timeout=15
)
print("\nSample attachment URLs:")
print(stdout.read().decode().strip())

# Check theme thumbnail display
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'the_post_thumbnail\|get_the_post_thumbnail' /www/wwwroot/resource_site/wp-content/themes/yymarket/*.php | head -10",
    timeout=10
)
print("\nTheme thumbnail calls:")
print(stdout.read().decode().strip())

ssh.close()