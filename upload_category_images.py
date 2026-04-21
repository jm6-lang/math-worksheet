import paramiko
import requests
import os

# Connect to server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sftp = ssh.open_sftp()

# Use placehold.co with resource-related keywords as text
# Categories: 小说, 影视, 网赚, 教程, AI, PPT

category_images = {
    'novel': 'https://placehold.co/600x400/4a90d9/ffffff?text=小说资源',
    'movie': 'https://placehold.co/600x400/e74c3c/ffffff?text=影视资源',
    'money': 'https://placehold.co/600x400/27ae60/ffffff?text=网赚项目',
    'course': 'https://placehold.co/600x400/f39c12/ffffff?text=教程合集',
    'ai': 'https://placehold.co/600x400/9b59b6/ffffff?text=AI工具',
    'ppt': 'https://placehold.co/600x400/1abc9c/ffffff?text=PPT模板',
    'default': 'https://placehold.co/600x400/34495e/ffffff?text=精品资源'
}

# Download and upload each category image
upload_dir = '/www/wwwroot/resource_site/wp-content/uploads/2026/04/'

for name, url in category_images.items():
    try:
        # Download
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            local_path = f'C:\\tmp\\{name}.png'
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            # Upload to server
            remote_path = f'{upload_dir}category_{name}.png'
            sftp.put(local_path, remote_path)
            print(f"Uploaded {name}.png")
    except Exception as e:
        print(f"Error with {name}: {e}")

sftp.close()
ssh.close()
print("\nCategory images uploaded!")