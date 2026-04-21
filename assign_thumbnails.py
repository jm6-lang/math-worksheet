import paramiko
import random

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Get all posts without thumbnails
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID NOT IN (SELECT post_id FROM wp_postmeta WHERE meta_key='_thumbnail_id')\" --allow-root",
    timeout=15
)
posts_without = [line.strip() for line in stdout.read().decode().strip().split('\n')[1:] if line.strip()]
print(f"Posts without thumbnails: {len(posts_without)}")

# Get all attachment IDs
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='attachment'\" --allow-root",
    timeout=15
)
attachments = [line.strip() for line in stdout.read().decode().strip().split('\n')[1:] if line.strip()]
print(f"Available attachments: {len(attachments)}")

# Assign random thumbnails to posts without them
batch_size = 50
for i, post_id in enumerate(posts_without[:200]):  # Limit to 200 for now
    thumb_id = random.choice(attachments)
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && wp post meta add {post_id} _thumbnail_id {thumb_id} --allow-root 2>&1",
        timeout=10
    )
    if i % 50 == 0:
        print(f"Processed {i} posts...")

print(f"\nAssigned thumbnails to {min(200, len(posts_without))} posts")

ssh.close()