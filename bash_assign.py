import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Simple approach - use WP CLI to set thumbnail for each post
# Get remaining posts
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID NOT IN (SELECT post_id FROM wp_postmeta WHERE meta_key='_thumbnail_id')\" --allow-root 2>&1 | tail -n +2",
    timeout=15
)
posts = [l.strip() for l in stdout.read().decode().strip().split('\n') if l.strip()]
print(f"Posts needing thumbnails: {len(posts)}")

# Get attachments
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='attachment' ORDER BY ID DESC LIMIT 30\" --allow-root 2>&1 | tail -n +2",
    timeout=15
)
attachments = [l.strip() for l in stdout.read().decode().strip().split('\n') if l.strip()]
print(f"Attachments: {len(attachments)}")

# Create a simple bash script
script_lines = ['#!/bin/bash', 'cd /www/wwwroot/resource_site']
for i, post_id in enumerate(posts):
    thumb = attachments[i % len(attachments)]
    script_lines.append(f'wp post meta add {post_id} _thumbnail_id {thumb} --allow-root 2>/dev/null || true')

script = '\n'.join(script_lines)

# Save script
sftp = ssh.open_sftp()
with sftp.open('/tmp/assign_thumbs.sh', 'w') as f:
    f.write(script)
sftp.close()

# Make executable and run
stdin, stdout, stderr = ssh.exec_command(
    "chmod +x /tmp/assign_thumbs.sh && /tmp/assign_thumbs.sh",
    timeout=120
)
print("\nRunning script...")
print(stdout.read().decode()[:500])
print("Errors:", stderr.read().decode()[:200])

ssh.close()