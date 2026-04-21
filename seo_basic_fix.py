import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 1. 更新WordPress网站标题和描述
cmd = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
UPDATE wp_options SET option_value = '小二郎资源网 - 副业项目教程资源平台' WHERE option_name = 'blogdescription';
SELECT option_name, option_value FROM wp_options WHERE option_name = 'blogdescription';
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("=== 更新网站描述 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 2. 更新首页SEO (Rank Math)
cmd2 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
UPDATE wp_postmeta SET meta_value = '小二郎资源网是专业的副业项目教程资源平台，提供网赚项目、线上兼职、技能变现、AI工具等优质互联网资源，帮助用户发现和获取有价值的副业赚钱内容。' WHERE post_id = 2 AND meta_key = 'rank_math_description';
SELECT * FROM wp_postmeta WHERE post_id = 2 AND meta_key = 'rank_math_description';
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== 更新Rank Math描述 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 3. 清理缓存
cmd3 = 'rm -rf /www/wwwroot/resource_site/wp-content/cache/* 2>/dev/null; echo "缓存已清理"'
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== 缓存 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 4. 检查并修复主题的header.php中的meta描述
cmd4 = 'grep -n "meta.*description" /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php 2>/dev/null | head -5'
stdin, stdout, stderr = ssh.exec_command(cmd4, timeout=30)
print("\n=== 主题Header meta检查 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 5. 检查是否有Rank Math的全局设置
cmd5 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT option_name, option_value FROM wp_options WHERE option_name = 'rank-math-options-general';
" | head -20
'''
stdin, stdout, stderr = ssh.exec_command(cmd5, timeout=30)
print("\n=== Rank Math全局设置 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
print("\n基本SEO优化完成")