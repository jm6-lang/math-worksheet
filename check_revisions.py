import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 检查是否有修订版本（revisions）
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT COUNT(*) FROM wp_posts WHERE post_type='revision';
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("修订版本数量: %s" % stdout.read().decode().strip())

# 检查最近几篇的修订版本
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT p.ID, p.post_parent, LEFT(p.post_content, 200)
FROM wp_posts p
WHERE p.post_type='revision' AND p.post_parent IN (26,27,28,29,30,31)
ORDER BY p.post_parent, p.ID DESC
LIMIT 10;
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
result = stdout.read().decode('utf-8', errors='ignore')
if result.strip():
    print("\n有修订版本！样本:")
    for line in result.strip().split('\n'):
        parts = line.split('\t')
        if len(parts) >= 3:
            has_link = '链接' in parts[2] or 'pan.baidu' in parts[2] or 'aliyundrive' in parts[2] or 'quark' in parts[2] or '网盘' in parts[2]
            print("  revision_id=%s, parent=%s, 有链接=%s" % (parts[0], parts[1], has_link))
else:
    print("没有找到修订版本")

# 看看原始文章有没有网盘链接的特征
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT COUNT(*) FROM wp_posts 
WHERE post_type='revision' 
AND (post_content LIKE '%pan.baidu%' OR post_content LIKE '%aliyundrive%' OR post_content LIKE '%quark%' OR post_content LIKE '%网盘%' OR post_content LIKE '%提取码%' OR post_content LIKE '%密码%');
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("\n含网盘链接的修订版本: %s" % stdout.read().decode().strip())

# 也看看有没有自动备份
cmd = """ls -la /www/wwwroot/resource_site/wp-content/backups/ 2>/dev/null || ls -la /www/wwwroot/resource_site/backups/ 2>/dev/null || echo 'no backup dir'"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("备份目录: %s" % stdout.read().decode().strip())

# 检查db备份
cmd = """ls -la /www/backup/ 2>/dev/null | head -10; ls -la /www/backup/database/ 2>/dev/null | head -10; echo '---'"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("DB备份: %s" % stdout.read().decode('utf-8', errors='ignore').strip())

ssh.close()
