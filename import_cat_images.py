import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# First, let's properly import the category images to media library
upload_dir = '/www/wwwroot/resource_site/wp-content/uploads/2026/04/'

# Import images using WP CLI
images = {
    'novel': '小说资源',
    'movie': '影视资源', 
    'money': '网赚项目',
    'course': '教程合集',
    'ai': 'AI工具',
    'ppt': 'PPT模板',
    'default': '精品资源'
}

image_ids = {}

for key, name in images.items():
    file_path = f"{upload_dir}category_{key}.png"
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && wp media import {file_path} --title='{name}' --porcelain --allow-root 2>&1",
        timeout=15
    )
    result = stdout.read().decode().strip()
    if result and result.isdigit():
        image_ids[key] = result
        print(f"{name}: ID {result}")
    else:
        print(f"{name}: Failed - {result}")

print(f"\nImage IDs: {image_ids}")

# Save mapping
with open('image_map.txt', 'w') as f:
    for k, v in image_ids.items():
        f.write(f"{k}:{v}\n")

ssh.close()