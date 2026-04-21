import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Check process
stdin, stdout, stderr = ssh.exec_command('ps aux | grep all_curl_img | grep -v grep', timeout=10)
print('Process:', stdout.read().decode('utf-8', errors='replace').strip())

# Check log
stdin, stdout, stderr = ssh.exec_command('tail -20 /root/scripts/add_img_batch2.txt', timeout=10)
print('\nLog:', stdout.read().decode('utf-8', errors='replace'))

# Check media count
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"attachment\" AND post_mime_type LIKE \"image/%%\"' 2>/dev/null",
    timeout=10
)
print('\n媒体库图片总数:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()