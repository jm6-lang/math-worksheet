import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Get all post IDs that don't have featured images yet
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp post list --post_type=post --fields=ID --format=csv --allow-root",
    timeout=15
)
all_posts = [l.strip() for l in stdout.read().decode().strip().split('\n')[1:] if l.strip()]

# Check which posts already have thumbnails
posts_need_images = []
for post_id in all_posts:
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && wp post meta get {post_id} _thumbnail_id --allow-root 2>&1",
        timeout=5
    )
    result = stdout.read().decode().strip()
    # If empty or error, post needs image
    if not result or 'Error' in result or not result.isdigit():
        posts_need_images.append(post_id)

print(f"Total posts: {len(all_posts)}")
print(f"Posts needing images: {len(posts_need_images)}")

if not posts_need_images:
    print("All posts already have featured images!")
    ssh.close()
    exit()

# Process all posts that need images
batch_size = 10
total = len(posts_need_images)
success = 0

print(f"\nProcessing {total} posts...")

for batch_start in range(0, total, batch_size):
    batch_end = min(batch_start + batch_size, total)
    batch_posts = posts_need_images[batch_start:batch_end]
    
    print(f"\n[{batch_start+1}-{batch_end}/{total}] Downloading images...")
    
    # Download fresh images for this batch
    for i in range(len(batch_posts)):
        seed = batch_start + i + 500  # Use different seeds
        stdin, stdout, stderr = ssh.exec_command(
            f"curl -sL 'https://picsum.photos/seed/{seed}/800/600' -o /tmp/batch_img_{i}.jpg",
            timeout=20
        )
        stdout.channel.recv_exit_status()
    
    # Import and assign
    print(f"Assigning images...")
    for i, post_id in enumerate(batch_posts):
        img_path = f"/tmp/batch_img_{i}.jpg"
        
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
                print(f"  {post_id}: OK")
            else:
                print(f"  {post_id}: Failed to assign")
        else:
            print(f"  {post_id}: Import failed")

print(f"\n=== COMPLETE ===")
print(f"Processed: {total}")
print(f"Success: {success}")
print(f"Failed: {total - success}")

ssh.close()