import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Kill any running scripts
ssh.exec_command("pkill -f batch_add_images")

# Get post count
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp post list --post_type=post --format=count --allow-root"
)
post_count = stdout.read().decode().strip()
print(f"Total posts: {post_count}")

# Simple loop - process 50 posts at a time
print("\nProcessing posts in batches of 50...")

for batch in range(0, 700, 50):
    print(f"\n=== Batch {batch}-{batch+50} ===")
    
    # Create a simple script for this batch
    script = f'''#!/bin/bash
cd /www/wwwroot/resource_site
offset={batch}
for i in $(seq 1 50); do
    post_id=$(wp post list --post_type=post --fields=ID --format=csv --offset=$offset --limit=1 --allow-root 2>/dev/null | tail -1)
    if [ -z "$post_id" ]; then break; fi
    
    # Check if has thumbnail
    thumb=$(wp post meta get $post_id _thumbnail_id --allow-root 2>/dev/null)
    if [ -n "$thumb" ]; then
        offset=$((offset + 1))
        continue
    fi
    
    # Download and assign
    seed=$((post_id + 10000))
    curl -sL "https://picsum.photos/seed/$seed/800/600" -o /tmp/img.jpg
    img_id=$(wp media import /tmp/img.jpg --porcelain --allow-root 2>/dev/null)
    if [ -n "$img_id" ]; then
        wp post meta update $post_id _thumbnail_id $img_id --allow-root >/dev/null
        echo "Post $post_id: OK"
    else
        echo "Post $post_id: FAIL"
    fi
    offset=$((offset + 1))
done
'''
    # Write and run
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/batch.sh', 'w') as f:
        f.write(script)
    sftp.close()
    
    stdin, stdout, stderr = ssh.exec_command("bash /tmp/batch.sh 2>&1", timeout=300)
    output = stdout.read().decode()
    print(output)
    
    # Count successes
    success_count = output.count(": OK")
    if success_count == 0:
        print("No more posts to process or all have images")
        break

print("\nDone!")
ssh.close()