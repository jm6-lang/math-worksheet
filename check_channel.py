import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 查找渠道资源分类
cmd = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT t.term_id, t.name, tt.count 
FROM wp_terms t 
JOIN wp_term_taxonomy tt ON t.term_id = tt.term_id 
WHERE t.name LIKE '%渠道%';
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("=== 渠道资源分类 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 查找渠道资源分类下的文章
cmd2 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT p.ID, p.post_title, LEFT(p.post_content, 200) as content_preview
FROM wp_posts p
JOIN wp_term_relationships tr ON p.ID = tr.object_id
JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
JOIN wp_terms t ON tt.term_id = t.term_id
WHERE t.name LIKE '%渠道%' AND p.post_type = 'post' AND p.post_status = 'publish'
ORDER BY p.ID DESC
LIMIT 10;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== 渠道资源文章预览 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 检查是否有二维码相关内容
cmd3 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT p.ID, p.post_title, 
       CASE WHEN p.post_content LIKE '%二维码%' THEN 'YES' ELSE 'NO' END as has_qrcode,
       CASE WHEN p.post_content LIKE '%pan.quark%' OR p.post_content LIKE '%pan.baidu%' OR p.post_content LIKE '%pan.xunlei%' THEN 'YES' ELSE 'NO' END as has_link
FROM wp_posts p
JOIN wp_term_relationships tr ON p.ID = tr.object_id
JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
JOIN wp_terms t ON tt.term_id = t.term_id
WHERE t.name LIKE '%渠道%' AND p.post_type = 'post' AND p.post_status = 'publish'
ORDER BY p.ID DESC
LIMIT 20;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== 渠道文章二维码和链接检查 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 查看一篇完整的渠道文章内容
cmd4 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT ID, post_title, post_content
FROM wp_posts
JOIN wp_term_relationships tr ON wp_posts.ID = tr.object_id
JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
JOIN wp_terms t ON tt.term_id = t.term_id
WHERE t.name LIKE '%渠道%' AND post_type = 'post' AND post_status = 'publish'
ORDER BY ID DESC
LIMIT 1;
" | head -100
'''
stdin, stdout, stderr = ssh.exec_command(cmd4, timeout=30)
print("\n=== 最新渠道文章完整内容 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
