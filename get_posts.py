import paramiko
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Get posts that need better thumbnails (with random ones assigned)
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT p.ID, p.post_title FROM wp_posts p WHERE p.post_type='post' AND p.post_status='publish' ORDER BY p.ID DESC LIMIT 50\" --allow-root",
    timeout=15
)
lines = stdout.read().decode('utf-8', errors='replace').strip().split('\n')[1:]

posts = []
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 2:
        posts.append((parts[0], parts[1]))

print(f"Got {len(posts)} posts")
for pid, title in posts[:10]:
    print(f"  {pid}: {title}")

ssh.close()

# Save for next step
with open('C:\\Users\\Administrator\\.qclaw\\workspace-agent-3bb7b585\\posts_to_fix.txt', 'w', encoding='utf-8') as f:
    for pid, title in posts:
        f.write(f"{pid}\t{title}\n")

print("\nSaved to posts_to_fix.txt")