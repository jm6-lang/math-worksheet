import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Total posts
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"post\" AND post_status=\"publish\"' 2>/dev/null",
    timeout=10
)
total = stdout.read().decode('utf-8', errors='replace').strip()
print('Total posts:', total)

# Posts with thumbnails
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_postmeta WHERE meta_key=\"_thumbnail_id\"' 2>/dev/null",
    timeout=10
)
with_thumb = stdout.read().decode('utf-8', errors='replace').strip()
print('With thumbnails:', with_thumb)

# Calculate remaining
try:
    total_num = int(total.split()[-1])
    thumb_num = int(with_thumb.split()[-1])
    print(f'Need images: {total_num - thumb_num}')
except:
    pass

ssh.close()