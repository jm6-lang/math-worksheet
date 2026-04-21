import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Kill slow process
ssh.exec_command("pkill -f full_import")

# Create faster script - just process all posts without checking
script = '''#!/bin/bash
LOG="/tmp/fast_import.log"
echo "Fast import started at $(date)" > $LOG_FILE

cd /www/wwwroot/resource_site

# Get all post IDs
wp post list --post_type=post --fields=ID --format=csv --allow-root | tail -n +2 > /tmp/all_posts.txt

total=$(wc -l < /tmp/all_posts.txt)
echo "Total posts to process: $total" >> $LOG

processed=0
success=0

while read post_id; do
    processed=$((processed + 1))
    
    # Download unique image for each post
    curl -sL "https://picsum.photos/seed/${post_id}/800/600" -o /tmp/img.jpg
    
    # Import
    img_id=$(wp media import /tmp/img.jpg --porcelain --allow-root 2>/dev/null)
    
    if [ -n "$img_id" ] && echo "$img_id" | grep -q '^[0-9]\+$'; then
        wp post meta update $post_id _thumbnail_id $img_id --allow-root >/dev/null 2>&1
        echo "[$processed/$total] Post $post_id -> Image $img_id: OK" >> $LOG
        success=$((success + 1))
    else
        echo "[$processed/$total] Post $post_id: FAIL" >> $LOG
    fi
    
    # Progress every 50
    if [ $((processed % 50)) -eq 0 ]; then
        echo "Progress: $processed/$total done ($success success)" >> $LOG
    fi
done < /tmp/all_posts.txt

echo "" >> $LOG
echo "=== DONE at $(date) ===" >> $LOG
echo "Total: $processed, Success: $success" >> $LOG
'''

# Upload and run
encoded = base64.b64encode(script.encode()).decode()
ssh.exec_command(f"echo '{encoded}' | base64 -d > /tmp/fast_import.sh && chmod +x /tmp/fast_import.sh", timeout=10)

print("Starting faster import process...")
ssh.exec_command("nohup bash /tmp/fast_import.sh > /dev/null 2>&1 &", timeout=5)

import time
time.sleep(3)

# Check
stdin, stdout, stderr = ssh.exec_command("ps aux | grep fast_import | grep -v grep")
if stdout.read().decode().strip():
    print("[OK] Fast import started")
else:
    print("[WARN] May not have started")

# Show initial log
stdin, stdout, stderr = ssh.exec_command("cat /tmp/fast_import.log 2>/dev/null || echo 'No log yet'")
print("\nLog:")
print(stdout.read().decode())

ssh.close()