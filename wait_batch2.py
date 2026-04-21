import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print('Waiting 3 minutes for batch 2 to complete...')
time.sleep(180)

# Check log
stdin, stdout, stderr = ssh.exec_command('cat /root/scripts/add_img_batch2.txt', timeout=10)
log = stdout.read().decode('utf-8', errors='replace')
print(log[-2000:] if len(log) > 2000 else log)

# Check total media count
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"attachment\" AND post_mime_type LIKE \"image/%%\"' 2>/dev/null",
    timeout=10
)
print('\n媒体库图片总数:', stdout.read().decode('utf-8', errors='replace').strip())

# Check how many posts still need images
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts p LEFT JOIN wp_postmeta pm ON p.ID=pm.post_id AND pm.meta_key=\"_thumbnail_id\" WHERE p.post_type=\"post\" AND p.post_status=\"publish\" AND pm.meta_id IS NULL' 2>/dev/null",
    timeout=10
)
print('还需要图片的文章:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()