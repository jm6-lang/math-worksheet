import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Simple approach: download images and use WP-CLI to import and assign
commands = [
    "cd /www/wwwroot/resource_site",
    "mkdir -p /tmp/article_images",
    "cd /tmp/article_images && curl -sL 'https://picsum.photos/seed/1/800/600' -o img1.jpg",
    "cd /tmp/article_images && curl -sL 'https://picsum.photos/seed/2/800/600' -o img2.jpg",
    "cd /tmp/article_images && curl -sL 'https://picsum.photos/seed/3/800/600' -o img3.jpg",
    "cd /tmp/article_images && curl -sL 'https://picsum.photos/seed/4/800/600' -o img4.jpg",
    "cd /tmp/article_images && curl -sL 'https://picsum.photos/seed/5/800/600' -o img5.jpg",
    "ls -la /tmp/article_images/",
]

print("Downloading sample images...")
for cmd in commands:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
    stdout.channel.recv_exit_status()

# Get some post IDs
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp post list --post_type=post --fields=ID --format=csv --allow-root | head -20",
    timeout=15
)
posts = [l.strip() for l in stdout.read().decode().strip().split('\n')[1:] if l.strip()]
print(f"\nFound {len(posts)} posts")

# Import images and assign
print("\nImporting images and assigning to posts...")
for i, post_id in enumerate(posts[:10]):
    img_num = (i % 5) + 1
    img_path = f"/tmp/article_images/img{img_num}.jpg"
    
    # Import image
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && wp media import {img_path} --porcelain --allow-root",
        timeout=15
    )
    result = stdout.read().decode().strip()
    
    if result.isdigit():
        img_id = result
        # Assign to post
        stdin, stdout, stderr = ssh.exec_command(
            f"cd /www/wwwroot/resource_site && wp post meta update {post_id} _thumbnail_id {img_id} --allow-root",
            timeout=10
        )
        assign_result = stdout.read().decode().strip()
        print(f"Post {post_id}: Image {img_id} - {assign_result}")
    else:
        print(f"Post {post_id}: Import failed - {result}")

ssh.close()
print("\nDone!")