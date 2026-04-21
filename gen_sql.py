import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Get posts still without thumbnails
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID NOT IN (SELECT post_id FROM wp_postmeta WHERE meta_key='_thumbnail_id') LIMIT 200\" --allow-root",
    timeout=15
)
posts = [l.strip() for l in stdout.read().decode().strip().split('\n')[1:] if l.strip()]
print(f"Remaining posts without thumbnails: {len(posts)}")

# Get attachment IDs
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='attachment' ORDER BY ID DESC LIMIT 50\" --allow-root",
    timeout=15
)
attachments = [l.strip() for l in stdout.read().decode().strip().split('\n')[1:] if l.strip()]
print(f"Attachments available: {len(attachments)}")

# Create SQL insert statements
sql_lines = []
for i, post_id in enumerate(posts[:150]):
    # Cycle through attachments
    thumb_id = attachments[i % len(attachments)]
    sql_lines.append(f"INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES ({post_id}, '_thumbnail_id', {thumb_id});")

sql = "\n".join(sql_lines)

# Save and execute
with open('/tmp/assign_thumbs2.sql', 'w', encoding='utf-8') as f:
    f.write(sql)

print(f"\nGenerated SQL for {len(posts[:150])} posts")
print("First 3 lines:")
print("\n".join(sql_lines[:3]))

ssh.close()