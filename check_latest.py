import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmd = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*), MAX(ID) FROM wp_posts WHERE post_type='post';\""
stdin, stdout, stderr = ssh.exec_command(cmd)
result = stdout.read().decode().strip()
print(f"Total posts: {result}", flush=True)

# Check last 30 titles
cmd2 = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT ID, post_title FROM wp_posts WHERE post_type='post' ORDER BY ID DESC LIMIT 30;\""
stdin, stdout, stderr = ssh.exec_command(cmd2)
lines = stdout.read().decode().strip().split('\n')
print(f"\nLast 30 posts:", flush=True)
for line in lines:
    parts = line.split('\t', 1)
    if len(parts) == 2:
        print(f"  {parts[0]}: {parts[1]}", flush=True)

ssh.close()
