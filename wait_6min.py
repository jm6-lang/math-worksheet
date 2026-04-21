import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Wait 6 minutes for 200 posts at 2s delay
print('Waiting 6 minutes for batch 4 to complete...')
time.sleep(360)

# Status check
stdin, stdout, stderr = ssh.exec_command('tail -5 /root/scripts/add_img_batch4.txt', timeout=10)
log_tail = stdout.read().decode('utf-8', errors='replace')
print('Log tail:', log_tail)

stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"attachment\" AND post_mime_type LIKE \"image/%%\"' 2>/dev/null",
    timeout=10
)
print('媒体库图片:', stdout.read().decode('utf-8', errors='replace').strip())

stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(DISTINCT post_id) FROM wp_postmeta WHERE meta_key=\"_thumbnail_id\"' 2>/dev/null",
    timeout=10
)
print('已有缩略图:', stdout.read().decode('utf-8', errors='replace').strip())

# Count posts without images
stdin, stdout, stderr = ssh.exec_command(
    '''mysql -u wpuser -p'WpPass2024!' wp_skillxm -e \"SELECT COUNT(*) FROM wp_posts p WHERE p.post_type='post' AND p.post_status='publish' AND NOT EXISTS (SELECT 1 FROM wp_postmeta pm WHERE pm.post_id=p.ID AND pm.meta_key='_thumbnail_id')\" 2>/dev/null''',
    timeout=10
)
print('还需图片:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()