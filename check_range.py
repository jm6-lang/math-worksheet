import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Check posts around ID 660-720
stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT ID, post_name FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID >= 660 AND ID <= 720 ORDER BY ID;\"")
posts = stdout.read().decode().strip()
print("Posts ID 660-720:")
for line in posts.split('\n'):
    print(line, flush=True)

ssh.close()
