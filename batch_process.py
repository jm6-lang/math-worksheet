import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Get all post IDs
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp post list --post_type=post --fields=ID --format=csv --allow-root",
    timeout=15
)
posts = [l.strip() for l in stdout.read().decode().strip().split('\n')[1:] if l.strip()]
print(f"Found {len(posts)} posts to process")

# Process in batches - download new images every 10 posts
batch_size = 10
total = len(posts)
success = 0

for batch_start in range(0, total, batch_size):
    batch_end = min(batch_start + batch_size, total)
    batch_posts = posts[batch_start:batch_end]
    
    print(f"\n=== Processing posts {batch_start+1}-{batch_end} of {total} ===")
    
    # Download fresh images for this batch
    for i in range(len(batch_posts)):
        seed = batch_start + i + 100
        stdin, stdout, stderr = ssh.exec_command(
            f"curl -sL 'https://picsum.photos/seed/{seed}/800/600' -o /tmp/article_img_{i}.jpg",
            timeout=20
        )
        stdout.channel.recv_exit_status()
    
    # Import and assign
    for i, post_id in enumerate(batch_posts):
        img_path = f"/tmp/article_img_{i}.jpg"
        
        # Import image
        stdin, stdout, stderr = ssh.exec_command(
            f"cd /www/wwwroot/resource_site && wp media import {img_path} --porcelain --allow-root 2>&1",
            timeout=15
        )
        result = stdout.read().decode().strip()
        
        if result.isdigit():
            img_id = result
            # Assign to post
            stdin, stdout, stderr = ssh.exec_command(
                f"cd /www/wwwroot/resource_site && wp post meta update {post_id} _thumbnail_id {img_id} --allow-root 2>&1",
                timeout=10
            )
            assign_result = stdout.read().decode().strip()
            if 'Success' in assign_result:
                success += 1
                print(f"  Post {post_id}: OK (img {img_id})")
            else:
                print(f"  Post {post_id}: Assign failed")
        else:
            print(f"  Post {post_id}: Import failed - {result[:50]}")

print(f"\n=== COMPLETE ===")
print(f"Total posts: {total}")
print(f"Success: {success}")
print(f"Failed: {total - success}")

ssh.close()