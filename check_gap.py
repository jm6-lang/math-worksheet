import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Count posts with book- or res- prefix in the range
stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID >= 662 AND ID <= 720;\"")
count = stdout.read().decode().strip()
print("Posts ID 662-720: {}".format(count), flush=True)

# Check if ID 710 is the last book/tool post
stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT ID, post_name FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID >= 700 ORDER BY ID LIMIT 20;\"")
posts = stdout.read().decode().strip()
print("\nPosts from ID 700:")
for line in posts.split('\n'):
    print(line, flush=True)

ssh.close()
