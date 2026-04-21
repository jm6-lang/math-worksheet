import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

upload_dir = '/www/wwwroot/resource_site/wp-content/uploads/2026/04/'

# Import each category image
images = ['novel', 'movie', 'money', 'course', 'ai', 'ppt', 'default']
image_ids = {}

for img in images:
    file_path = f'{upload_dir}category_{img}.png'
    
    # Import
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && wp media import {file_path} --allow-root 2>&1",
        timeout=15
    )
    result = stdout.read().decode()
    print(f"{img}: {result[:100]}")

# Get the IDs
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT ID, post_title FROM wp_posts WHERE post_type='attachment' AND post_date > '2026-04-07 08:20:00' ORDER BY ID ASC\" --allow-root",
    timeout=15
)
print("\nNew attachments:")
print(stdout.read().decode())

ssh.close()