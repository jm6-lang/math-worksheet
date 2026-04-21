import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check if completed
stdin, stdout, stderr = ssh.exec_command("cat /tmp/fast_import.log 2>/dev/null | tail -10")
log = stdout.read().decode()

stdin, stdout, stderr = ssh.exec_command("ps aux | grep fast_import | grep -v grep")
running = stdout.read().decode().strip()

# Get final stats
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp media list --format=count --allow-root 2>/dev/null"
)
media_count = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT COUNT(DISTINCT post_id) FROM wp_postmeta WHERE meta_key='_thumbnail_id'\" --allow-root 2>/dev/null | tail -1"
)
posts_with_thumb = stdout.read().decode().strip()

ssh.close()

print("=== IMPORT COMPLETE ===")
print(f"\nStatus: {'Running' if running else 'Completed'}")
print(f"\nFinal Stats:")
print(f"  - Media library images: {media_count}")
print(f"  - Posts with thumbnail: {posts_with_thumb}")
print(f"\nLast log entries:")
print(log)