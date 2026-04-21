import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Kill any hanging processes
ssh.exec_command("pkill -f 'batch_add_images|batch.sh'")

# Create a comprehensive script that runs in background
script = '''#!/bin/bash
LOG_FILE="/tmp/image_import.log"
echo "Starting image import at $(date)" > $LOG_FILE

cd /www/wwwroot/resource_site

# Get all posts needing images
echo "Checking posts..." >> $LOG_FILE
wp post list --post_type=post --fields=ID --format=csv --allow-root | tail -n +2 > /tmp/posts_to_check.txt

total=$(wc -l < /tmp/posts_to_check.txt)
echo "Total posts: $total" >> $LOG_FILE

need_count=0
> /tmp/posts_need_images.txt

while read post_id; do
    thumb=$(wp post meta get $post_id _thumbnail_id --allow-root 2>/dev/null)
    if [ -z "$thumb" ]; then
        echo $post_id >> /tmp/posts_need_images.txt
        need_count=$((need_count + 1))
    fi
done < /tmp/posts_to_check.txt

echo "Posts needing images: $need_count" >> $LOG_FILE

if [ $need_count -eq 0 ]; then
    echo "All posts already have images!" >> $LOG_FILE
    exit 0
fi

# Process all
processed=0
success=0
while read post_id; do
    processed=$((processed + 1))
    
    # Download
    seed=$((post_id + 5000))
    curl -sL "https://picsum.photos/seed/$seed/800/600" -o /tmp/img_$post_id.jpg
    
    # Import
    img_id=$(wp media import /tmp/img_$post_id.jpg --porcelain --allow-root 2>/dev/null)
    
    if [ -n "$img_id" ] && echo "$img_id" | grep -q '^[0-9]\+$'; then
        wp post meta update $post_id _thumbnail_id $img_id --allow-root >/dev/null 2>&1
        echo "[$processed/$need_count] Post $post_id -> Image $img_id: SUCCESS" >> $LOG_FILE
        success=$((success + 1))
    else
        echo "[$processed/$need_count] Post $post_id: FAILED (import error)" >> $LOG_FILE
    fi
    
    # Cleanup
    rm -f /tmp/img_$post_id.jpg
    
    # Progress update every 20
    if [ $((processed % 20)) -eq 0 ]; then
        echo "Progress: $processed/$need_count done, $success success" >> $LOG_FILE
    fi
    
    # Small delay to be nice to the server
    sleep 0.5
done < /tmp/posts_need_images.txt

echo "" >> $LOG_FILE
echo "=== COMPLETE at $(date) ===" >> $LOG_FILE
echo "Total: $processed, Success: $success, Failed: $((processed - success))" >> $LOG_FILE
'''

# Upload and run in background
encoded = base64.b64encode(script.encode()).decode()
stdin, stdout, stderr = ssh.exec_command(
    f"echo '{encoded}' | base64 -d > /tmp/full_import.sh && chmod +x /tmp/full_import.sh",
    timeout=10
)

print("Starting background import process...")
print("This will process all posts and save results to /tmp/image_import.log")
print("")

# Run in background with nohup
stdin, stdout, stderr = ssh.exec_command(
    "nohup bash /tmp/full_import.sh > /dev/null 2>&1 &",
    timeout=5
)

# Wait a moment and check if it started
import time
time.sleep(2)

stdin, stdout, stderr = ssh.exec_command("ps aux | grep full_import | grep -v grep")
if stdout.read().decode().strip():
    print("✓ Background process started successfully")
    print("")
    print("To check progress, run:")
    print("  tail -f /tmp/image_import.log")
    print("")
    print("Current log (if any):")
    stdin, stdout, stderr = ssh.exec_command("cat /tmp/image_import.log 2>/dev/null || echo 'Log not created yet'")
    print(stdout.read().decode())
else:
    print("✗ Process did not start")

ssh.close()