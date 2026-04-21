import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Quick check: is there any new images uploaded in last 5 minutes?
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT ID, post_title, post_date FROM wp_posts WHERE post_type=\"attachment\" ORDER BY ID DESC LIMIT 5' 2>/dev/null",
    timeout=10
)
print("Recent attachments:")
print(stdout.read().decode('utf-8', errors='replace'))

# Check HTTP connectivity from server
stdin, stdout, stderr = ssh.exec_command(
    "curl -s -o /dev/null -w '%{http_code}' --max-time 5 https://loremflickr.com/800/600/business",
    timeout=10
)
print("\nServer->LoremFlickr:", stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()