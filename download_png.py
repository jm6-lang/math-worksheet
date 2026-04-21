import paramiko
import requests

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

upload_dir = '/www/wwwroot/resource_site/wp-content/uploads/2026/04/'

# Download proper PNG images from placehold.co
categories = {
    'novel': ('小说资源', '4a90d9'),
    'movie': ('影视资源', 'e74c3c'),
    'money': ('网赚项目', '27ae60'),
    'course': ('教程合集', 'f39c12'),
    'ai': ('AI工具', '9b59b6'),
    'ppt': ('PPT模板', '1abc9c'),
    'default': ('精品资源', '34495e')
}

sftp = ssh.open_sftp()

for key, (name, color) in categories.items():
    # Download PNG with proper format
    url = f"https://placehold.co/600x400/{color}/ffffff/png?text={name}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            # Save locally first
            local_path = f'C:\\tmp\\cat_{key}.png'
            with open(local_path, 'wb') as f:
                f.write(r.content)
            
            # Upload to server
            remote_path = f'{upload_dir}cat_{key}.png'
            sftp.put(local_path, remote_path)
            print(f"Uploaded {name}")
    except Exception as e:
        print(f"Error with {name}: {e}")

sftp.close()

# Fix permissions
stdin, stdout, stderr = ssh.exec_command(
    f"chown www-data:www-data {upload_dir}cat_*.png && chmod 644 {upload_dir}cat_*.png",
    timeout=10
)

# Verify file types
stdin, stdout, stderr = ssh.exec_command(
    f"file {upload_dir}cat_*.png",
    timeout=10
)
print("\nFile types after upload:")
print(stdout.read().decode())

ssh.close()