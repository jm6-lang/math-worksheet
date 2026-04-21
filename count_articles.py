import paramiko, sys, json
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 获取文章统计：按分类统计数量
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT t.name, COUNT(DISTINCT p.ID) as cnt
FROM wp_posts p
JOIN wp_term_relationships tr ON p.ID = tr.object_id
JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
JOIN wp_terms t ON tt.term_id = t.term_id
WHERE p.post_type='post' AND p.post_status='publish' AND tt.taxonomy='category'
GROUP BY t.term_id ORDER BY cnt DESC;
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("=== 文章按分类统计 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 总数
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT COUNT(*) FROM wp_posts WHERE post_type='post' AND post_status='publish';
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("总文章数: %s" % stdout.read().decode().strip())

# 取几个样本标题看看
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT p.ID, p.post_title, t.name
FROM wp_posts p
LEFT JOIN wp_term_relationships tr ON p.ID = tr.object_id
LEFT JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
LEFT JOIN wp_terms t ON tt.term_id = t.term_id AND tt.taxonomy='category'
WHERE p.post_type='post' AND p.post_status='publish'
ORDER BY RAND() LIMIT 10;
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("\n=== 随机10篇样本 ===")
for line in stdout.read().decode('utf-8', errors='ignore').strip().split('\n'):
    parts = line.split('\t')
    if len(parts) >= 2:
        print("  [%s] %s (%s)" % (parts[0], parts[1][:50], parts[2] if len(parts) > 2 else '?'))

ssh.close()
