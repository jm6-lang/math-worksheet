import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 检查文章的修订版本
cmd = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT ID, post_parent, post_title, LEFT(post_content, 300) as content_preview, post_date
FROM wp_posts 
WHERE post_parent IN (779, 737) AND post_type = 'revision'
ORDER BY post_parent, post_date DESC;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("=== 文章修订版本 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 检查渠道资源分类下所有文章
cmd2 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT p.ID, p.post_title, p.post_date
FROM wp_posts p
JOIN wp_term_relationships tr ON p.ID = tr.object_id
JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
JOIN wp_terms t ON tt.term_id = t.term_id
WHERE t.name LIKE '%渠道%' AND p.post_type = 'post' AND p.post_status = 'publish'
ORDER BY p.ID;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== 所有渠道资源文章 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 检查postmeta中是否有原始数据
cmd3 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT post_id, meta_key, LEFT(meta_value, 200) as meta_value
FROM wp_postmeta 
WHERE post_id IN (779, 737) 
AND (meta_key LIKE '%qr%' OR meta_key LIKE '%code%' OR meta_key LIKE '%link%' OR meta_key LIKE '%url%')
LIMIT 20;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== 文章meta数据 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
