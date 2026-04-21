import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create SQL to assign thumbnails in bulk
sql = """
SET @attachments = (SELECT GROUP_CONCAT(ID) FROM wp_posts WHERE post_type='attachment');

INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT 
    p.ID as post_id,
    '_thumbnail_id' as meta_key,
    (SELECT ID FROM wp_posts WHERE post_type='attachment' ORDER BY RAND() LIMIT 1) as meta_value
FROM wp_posts p
WHERE p.post_type = 'post' 
  AND p.post_status = 'publish'
  AND p.ID NOT IN (SELECT post_id FROM wp_postmeta WHERE meta_key = '_thumbnail_id')
LIMIT 400;
"""

# Save SQL to file
sftp = ssh.open_sftp()
with sftp.open('/tmp/assign_thumbs.sql', 'w') as f:
    f.write(sql)
sftp.close()

# Execute SQL
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query < /tmp/assign_thumbs.sql --allow-root 2>&1",
    timeout=60
)
print("Result:", stdout.read().decode().strip())
print("Errors:", stderr.read().decode().strip())

# Check result
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT COUNT(DISTINCT post_id) FROM wp_postmeta WHERE meta_key='_thumbnail_id'\" --allow-root",
    timeout=15
)
print("\nPosts with thumbnails after update:", stdout.read().decode().strip())

ssh.close()