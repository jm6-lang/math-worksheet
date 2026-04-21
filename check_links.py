import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 看看重写后的文章内容里有没有任何链接
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT COUNT(*) as total,
    SUM(CASE WHEN post_content LIKE '%pan.baidu%' THEN 1 ELSE 0 END) as baidu,
    SUM(CASE WHEN post_content LIKE '%aliyundrive%' OR post_content LIKE '%alipan%' THEN 1 ELSE 0 END) as ali,
    SUM(CASE WHEN post_content LIKE '%quark%' OR post_content LIKE '%夸克%' THEN 1 ELSE 0 END) as quark,
    SUM(CASE WHEN post_content LIKE '%http%' THEN 1 ELSE 0 END) as any_link,
    SUM(CASE WHEN post_content LIKE '%提取码%' OR post_content LIKE '%密码%' THEN 1 ELSE 0 END) as has_pwd
FROM wp_posts WHERE post_type='post' AND post_status='publish' AND post_title!='Hello world!';
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("当前文章链接统计:")
print(stdout.read().decode().strip())

ssh.close()
