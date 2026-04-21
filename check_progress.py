import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check output file if any
stdin, stdout, stderr = ssh.exec_command("ls -la /tmp/all_posts.txt 2>&1")
print("Posts file:", stdout.read().decode())

# Count how many images have been added
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp media list --fields=ID --format=csv --allow-root 2>/dev/null | wc -l"
)
media_count = stdout.read().decode().strip()
print(f"Media items: {media_count}")

# Check a few posts
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp post list --post_type=post --fields=ID --format=csv --allow-root | head -5"
)
print("\nSample posts:")
print(stdout.read().decode())

ssh.close()