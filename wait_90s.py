import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print('Waiting 1.5 more minutes...')
time.sleep(90)

# Quick status
stdin, stdout, stderr = ssh.exec_command('tail -10 /root/scripts/add_img_batch3.txt', timeout=10)
print('Log:', stdout.read().decode('utf-8', errors='replace'))

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

ssh.close()