import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

upload_dir = '/www/wwwroot/resource_site/wp-content/uploads/2026/04/'

# Import category images
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
    file_path = f"{upload_dir}cat_{key}.png"
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && wp media import {file_path} --title='{name}' --porcelain --allow-root 2>&1",
        timeout=15
    )
    result = stdout.read().decode().strip()
    if result.isdigit():
        image_ids[key] = result
        print(f"{name}: ID {result}")
    else:
        print(f"{name}: {result}")

print(f"\nImage IDs: {image_ids}")

# Now assign images to posts based on category
# Get category mappings
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT t.term_id, t.name FROM wp_terms t JOIN wp_term_taxonomy tt ON t.term_id = tt.term_id WHERE tt.taxonomy='category'\" --allow-root",
    timeout=15
)
cats = stdout.read().decode('utf-8', errors='replace')
print("\nCategories:")
print(cats)

ssh.close()

# Save image mapping
with open('C:\\Users\\Administrator\\.qclaw\\workspace-agent-3bb7b585\\image_ids.txt', 'w') as f:
    for k, v in image_ids.items():
        f.write(f"{k}:{v}\n")