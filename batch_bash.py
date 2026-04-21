import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create a bash script to run on server
bash_script = '''#!/bin/bash
cd /www/wwwroot/resource_site

echo "Getting posts without featured images..."

# Get all post IDs
wp post list --post_type=post --fields=ID --format=csv --allow-root | tail -n +2 > /tmp/all_posts.txt

total=$(wc -l < /tmp/all_posts.txt)
echo "Total posts: $total"

# Check which need images
need_images=""
count=0
while read post_id; do
    thumb=$(wp post meta get $post_id _thumbnail_id --allow-root 2>/dev/null)
    if [ -z "$thumb" ] || [ "$thumb" = "" ]; then
        need_images="$need_images $post_id"
        count=$((count + 1))
    fi
done < /tmp/all_posts.txt

echo "Posts needing images: $count"

if [ $count -eq 0 ]; then
    echo "All posts already have images!"
    exit 0
fi

# Process in batches
batch_size=20
processed=0
success=0

for post_id in $need_images; do
    processed=$((processed + 1))
    
    # Download image
    seed=$((processed + 1000))
    curl -sL "https://picsum.photos/seed/$seed/800/600" -o /tmp/article_img.jpg
    
    # Import
    img_id=$(wp media import /tmp/article_img.jpg --porcelain --allow-root 2>/dev/null)
    
    if [ -n "$img_id" ] && [ "$img_id" -eq "$img_id" ] 2>/dev/null; then
        # Assign
        wp post meta update $post_id _thumbnail_id $img_id --allow-root >/dev/null 2>&1
        echo "[$processed/$count] Post $post_id: OK (img $img_id)"
        success=$((success + 1))
    else
        echo "[$processed/$count] Post $post_id: FAILED"
    fi
    
    # Progress every 10
    if [ $((processed % 10)) -eq 0 ]; then
        echo "--- Progress: $processed/$count ---"
    fi
done

echo ""
echo "=== COMPLETE ==="
echo "Processed: $processed"
echo "Success: $success"
echo "Failed: $((processed - success))"
'''

# Upload via base64
encoded = base64.b64encode(bash_script.encode()).decode()
stdin, stdout, stderr = ssh.exec_command(
    f"echo '{encoded}' | base64 -d > /tmp/batch_add_images.sh && chmod +x /tmp/batch_add_images.sh",
    timeout=10
)

print("Bash script created on server")
print("\nRunning batch process (this will take several minutes)...")
print("=" * 60)

# Run the script
stdin, stdout, stderr = ssh.exec_command(
    "bash /tmp/batch_add_images.sh 2>&1",
    timeout=600
)

# Stream output
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        chunk = stdout.channel.recv(1024).decode('utf-8', errors='replace')
        print(chunk, end='')

# Get remaining
remaining = stdout.read().decode('utf-8', errors='replace')
if remaining:
    print(remaining)

err = stderr.read().decode('utf-8', errors='replace')
if err:
    print("Errors:", err[:500])

print("=" * 60)
print("Done!")

ssh.close()