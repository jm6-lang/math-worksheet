import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print('Waiting 45 seconds...')
time.sleep(45)

# Check log
stdin, stdout, stderr = ssh.exec_command('cat /root/scripts/add_img_log4.txt', timeout=10)
print(stdout.read().decode('utf-8', errors='replace'))

# Check image count
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"attachment\" AND post_mime_type LIKE \"image/%%\"' 2>/dev/null",
    timeout=10
)
print('\n媒体库图片数:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()