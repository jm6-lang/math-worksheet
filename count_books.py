import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Count book- posts
stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_posts WHERE post_type='post' AND post_status='publish' AND post_name LIKE 'book-%';\"")
book_count = stdout.read().decode().strip()
print("Book posts (book- prefix): {}".format(book_count), flush=True)

# Get the range of book posts
stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT MIN(ID), MAX(ID) FROM wp_posts WHERE post_type='post' AND post_status='publish' AND post_name LIKE 'book-%';\"")
book_range = stdout.read().decode().strip()
print("Book ID range: {}".format(book_range), flush=True)

ssh.close()
