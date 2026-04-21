import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Check processes
stdin, stdout, stderr = ssh.exec_command('ps aux | grep all_curl_img | grep -v grep', timeout=10)
print('Running:', stdout.read().decode('utf-8', errors='replace').strip())

# Check batch4 log
stdin, stdout, stderr = ssh.exec_command('tail -15 /root/scripts/add_img_batch4.txt', timeout=10)
print('\nBatch4 log:', stdout.read().decode('utf-8', errors='replace'))

# Media count
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"attachment\" AND post_mime_type LIKE \"image/%%\"' 2>/dev/null",
    timeout=10
)
print('\n媒体库:', stdout.read().decode('utf-8', errors='replace').strip())

# Posts with thumbs
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_postmeta WHERE meta_key=\"_thumbnail_id\"' 2>/dev/null",
    timeout=10
)
print('有缩略图:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()