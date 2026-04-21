import paramiko
from datetime import datetime
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Check latest post count
cmd = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*), MAX(ID) FROM wp_posts WHERE post_type='post';\""
stdin, stdout, stderr = ssh.exec_command(cmd)
print("Status:", stdout.read().decode().strip())

# Check if the issue is stdout buffering - use print flush
print("Testing publish with echo...", flush=True)

CAT_MOVIE = 86
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
title = "测试影视文章"
content = "<p>测试</p>"
post_name = f"test-{int(time.time())}"
sql = f"INSERT INTO wp_posts (post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt, post_content_filtered, post_parent, guid, menu_order, post_type, post_mime_type, comment_count) VALUES (1, '{now}', '{now}', '{content}', '{title}', '', 'publish', 'open', 'open', '', '{post_name}', '', '', '{now}', '{now}', '', 0, '', 0, 'post', '', 0);"

# Write SQL file
sftp = ssh.open_sftp()
with sftp.open('/tmp/wp_test.sql', 'w') as f:
    f.write(sql)
sftp.close()

cmd = "mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_test.sql 2>&1 && echo 'INSERT_OK'"
stdin, stdout, stderr = ssh.exec_command(cmd)
result = stdout.read().decode()
print(f"Insert result: {result}", flush=True)

# Check
cmd2 = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*), MAX(ID) FROM wp_posts WHERE post_type='post';\""
stdin, stdout, stderr = ssh.exec_command(cmd2)
print(f"After: {stdout.read().decode().strip()}", flush=True)

# Cleanup
ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"DELETE FROM wp_posts WHERE post_title='测试影视文章';\"")

ssh.close()
print("Done", flush=True)
