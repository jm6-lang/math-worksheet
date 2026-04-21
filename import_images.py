import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Add uploaded images to media library and get their IDs
upload_dir = '/www/wwwroot/resource_site/wp-content/uploads/2026/04/'

categories = {
    'novel': '小说资源',
    'movie': '影视资源',
    'money': '网赚项目',
    'course': '教程合集',
    'ai': 'AI工具',
    'ppt': 'PPT模板',
    'default': '精品资源'
}

image_ids = {}

for key, name in categories.items():
    file_path = f'{upload_dir}category_{key}.png'
    
    # Import to media library
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && wp media import {file_path} --title='{name}' --alt='{name}' --allow-root 2>&1",
        timeout=15
    )
    result = stdout.read().decode()
    
    # Extract attachment ID
    if 'Success:' in result:
        # Get the attachment ID from the file
        stdin, stdout, stderr = ssh.exec_command(
            f"cd /www/wwwroot/resource_site && wp db query \"SELECT ID FROM wp_posts WHERE post_type='attachment' AND guid LIKE '%category_{key}.png%' ORDER BY ID DESC LIMIT 1\" --allow-root",
            timeout=10
        )
        id_result = stdout.read().decode().strip()
        if id_result and id_result != 'ID':
            image_ids[key] = id_result.split('\n')[-1].strip()
            print(f"{name}: ID {image_ids[key]}")

print(f"\nImage IDs: {image_ids}")

ssh.close()

# Save for next step
with open('C:\\Users\\Administrator\\.qclaw\\workspace-agent-3bb7b585\\image_ids.txt', 'w') as f:
    for k, v in image_ids.items():
        f.write(f"{k}:{v}\n")