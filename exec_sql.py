import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Read SQL file
with open('/tmp/assign_thumbs2.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

# Upload to server
sftp = ssh.open_sftp()
with sftp.open('/tmp/assign_thumbs2.sql', 'w') as f:
    f.write(sql)
sftp.close()

# Execute in smaller batches
lines = sql.strip().split('\n')
batch_size = 30

for i in range(0, len(lines), batch_size):
    batch = "\n".join(lines[i:i+batch_size])
    # Write batch
    with sftp.open('/tmp/batch.sql', 'w') as f:
        f.write(batch)
    
    # Execute
    stdin, stdout, stderr = ssh.exec_command(
        "cd /www/wwwroot/resource_site && wp db query < /tmp/batch.sql --allow-root 2>&1",
        timeout=30
    )
    result = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    print(f"Batch {i//batch_size + 1}: {len(lines[i:i+batch_size])} posts")
    if err:
        print(f"  Error: {err[:100]}")

# Final check
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT COUNT(DISTINCT post_id) FROM wp_postmeta WHERE meta_key='_thumbnail_id'\" --allow-root",
    timeout=15
)
print("\nFinal posts with thumbnails:", stdout.read().decode().strip())

ssh.close()
print("Done!")