import paramiko
from datetime import datetime

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Test one article
title = 'test'
content = '<p>test</p>'
content_escaped = content
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

sql = f"""INSERT INTO wp_posts (
    post_author, post_date, post_date_gmt, post_content, post_title,
    post_excerpt, post_status, comment_status, ping_status,
    post_password, post_name, to_ping, pinged, post_modified,
    post_modified_gmt, post_content_filtered, post_parent, guid,
    menu_order, post_type, post_mime_type, comment_count
) VALUES (
    1, '{now}', '{now}', '{content_escaped}', '{title}',
    '', 'publish', 'open', 'open',
    '', 'test-post-2', '', '', '{now}',
    '{now}', '', 0, '',
    0, 'post', '', 0
);"""

cmd = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql}\""
print(f"Running test...")
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
err = stderr.read().decode()
if out:
    print(f"OUT: {out}")
if err:
    print(f"ERR: {err}")
if not out and not err:
    print("OK - no output means success")

# Check latest post
cmd2 = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"SELECT ID, post_title FROM wp_posts WHERE post_type='post' ORDER BY ID DESC LIMIT 3;\""
stdin, stdout, stderr = ssh.exec_command(cmd2)
print(stdout.read().decode())
print(stderr.read().decode())

# Clean up test post
cmd3 = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"DELETE FROM wp_posts WHERE post_title='test' AND post_type='post';\""
ssh.exec_command(cmd3)

ssh.close()
print("Test done")
