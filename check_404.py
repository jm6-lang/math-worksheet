import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 检查新创建的文章详情
cmd = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT ID, post_title, post_status, post_name, post_type 
FROM wp_posts 
WHERE ID >= 1825 
ORDER BY ID 
LIMIT 20;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("=== 新文章状态 ===")
print(stdout.read().decode('utf-8'))

# 检查wp_term_relationships是否有记录
cmd2 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT object_id, term_taxonomy_id 
FROM wp_term_relationships 
WHERE object_id >= 1825 
LIMIT 20;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== 分类关联 ===")
print(stdout.read().decode('utf-8'))

# 检查nginx错误日志
cmd3 = 'tail -20 /var/log/nginx/error.log 2>/dev/null || tail -20 /www/server/nginx/logs/error.log'
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== Nginx错误日志 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 测试访问一篇文章
cmd4 = 'curl -s -o /dev/null -w "%{http_code}" https://www.skillxm.cn/?p=1825'
stdin, stdout, stderr = ssh.exec_command(cmd4, timeout=30)
print("\n=== 测试文章ID 1825 ===")
print("HTTP状态码:", stdout.read().decode())

ssh.close()
