import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 查看渠道资源分类下的所有文章
cmd = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT p.ID, p.post_title, p.post_name, p.post_date
FROM wp_posts p
JOIN wp_term_relationships tr ON p.ID = tr.object_id
JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
JOIN wp_terms t ON tt.term_id = t.term_id
WHERE t.name LIKE '%渠道%' AND p.post_type = 'post' AND p.post_status = 'publish'
ORDER BY p.ID;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("=== 渠道资源分类文章 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 查看网站媒体库中的二维码图片
cmd2 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT ID, post_title, guid 
FROM wp_posts 
WHERE post_type = 'attachment' 
AND (post_title LIKE '%二维码%' OR post_title LIKE '%qr%' OR guid LIKE '%qr%')
ORDER BY ID DESC
LIMIT 20;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== 媒体库二维码图片 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 查看文章的特色图片
cmd3 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT pm.post_id, pm.meta_value 
FROM wp_postmeta pm
WHERE pm.meta_key = 'fifu_image_url' 
AND pm.post_id IN (SELECT ID FROM wp_posts WHERE post_type = 'post')
ORDER BY pm.post_id DESC
LIMIT 10;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== 文章特色图片URL ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 查看wp-content/uploads目录下的二维码图片
cmd4 = 'ls -la /www/wwwroot/resource_site/wp-content/uploads/ 2>/dev/null | head -30'
stdin, stdout, stderr = ssh.exec_command(cmd4, timeout=30)
print("\n=== uploads目录 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
