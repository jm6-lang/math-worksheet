import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Category to image mapping (based on term_id)
# 53=网赚项目->money(1087), 84=小说资源->novel(1085), 85=教程合集->course(1088)
# 86=影视资源->movie(1086), 91=资源合集->default(1091), 93=网创资源->money(1087)

cat_to_image = {
    '53': '1087',   # 网赚项目
    '84': '1085',   # 小说资源
    '85': '1088',   # 教程合集
    '86': '1086',   # 影视资源
    '91': '1091',   # 资源合集
    '93': '1087',   # 网创资源
}

# For each category, update posts to use the corresponding image
for cat_id, img_id in cat_to_image.items():
    print(f"\nProcessing category {cat_id} with image {img_id}...")
    
    # Get posts in this category
    stdin, stdout, stderr = ssh.exec_command(
        f"cd /www/wwwroot/resource_site && wp db query \"SELECT object_id FROM wp_term_relationships WHERE term_taxonomy_id IN (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id={cat_id})\" --allow-root",
        timeout=15
    )
    posts = [l.strip() for l in stdout.read().decode().strip().split('\n')[1:] if l.strip()]
    print(f"  Found {len(posts)} posts")
    
    # Update each post's thumbnail
    for post_id in posts[:100]:  # Limit to 100 per category for now
        stdin, stdout, stderr = ssh.exec_command(
            f"cd /www/wwwroot/resource_site && wp post meta update {post_id} _thumbnail_id {img_id} --allow-root 2>&1",
            timeout=10
        )
        result = stdout.read().decode().strip()
        if 'Success' not in result and 'Updated' not in result:
            print(f"    Post {post_id}: {result}")

print("\nDone! Refresh the site to see category-specific images.")

ssh.close()