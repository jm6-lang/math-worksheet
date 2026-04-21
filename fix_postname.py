import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 修复所有新文章的post_name为数字ID
cmd = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
UPDATE wp_posts SET post_name = ID WHERE ID >= 1825 AND post_type = 'post';
SELECT ID, post_title, post_name FROM wp_posts WHERE ID >= 1825 LIMIT 20;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("=== 修复后的文章 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 刷新WordPress缓存
cmd2 = '''
cd /www/wwwroot/resource_site
php -r "require 'wp-load.php'; flush_rewrite_rules(); echo 'Rewrite rules flushed\n';"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== 刷新重写规则 ===")
print(stdout.read().decode('utf-8', errors='ignore'))
err = stderr.read().decode('utf-8', errors='ignore')
if err:
    print("错误:", err)

# 测试访问
cmd3 = "curl -sIL 'https://www.skillxm.cn/?p=1825' 2>&1 | head -10"
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== 测试文章1825 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
