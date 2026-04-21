import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print('Waiting 2 more minutes...')
time.sleep(120)

# Quick status check
stdin, stdout, stderr = ssh.exec_command('tail -20 /root/scripts/add_img_batch3.txt', timeout=10)
print('Log:', stdout.read().decode('utf-8', errors='replace'))

stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"attachment\" AND post_mime_type LIKE \"image/%%\"' 2>/dev/null",
    timeout=10
)
print('\n媒体库图片总数:', stdout.read().decode('utf-8', errors='replace').strip())

# Check how many posts have featured images now
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(DISTINCT post_id) FROM wp_postmeta WHERE meta_key=\"_thumbnail_id\"' 2>/dev/null",
    timeout=10
)
print('已有缩略图的文章:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()