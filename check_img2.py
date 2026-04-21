import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Check posts with images
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e \"SELECT ID, post_title, LENGTH(post_content) as len, post_content FROM wp_posts WHERE post_type='post' AND post_status='publish' ORDER BY ID DESC LIMIT 2\" 2>/dev/null",
    timeout=10
)
print("最近文章内容片段:")
print(stdout.read().decode('utf-8', errors='replace'))

# Check how many posts have featured image (_thumbnail_id)
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e \"SELECT COUNT(*) as with_thumb FROM wp_postmeta WHERE meta_key='_thumbnail_id'\" 2>/dev/null",
    timeout=10
)
print("有缩略图的文章数:", stdout.read().decode('utf-8', errors='replace').strip())

# Check total posts
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e \"SELECT COUNT(*) as total_posts FROM wp_posts WHERE post_type='post' AND post_status='publish'\" 2>/dev/null",
    timeout=10
)
print("文章总数:", stdout.read().decode('utf-8', errors='replace').strip())

# Check image URLs in post content
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e \"SELECT ID, LEFT(post_content, 500) FROM wp_posts WHERE post_type='post' AND post_status='publish' LIMIT 1\" 2>/dev/null",
    timeout=10
)
print("文章内容示例:")
content = stdout.read().decode('utf-8', errors='replace')
print(content)

ssh.close()
