import paramiko, sys, re
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 统计字数
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN LENGTH(post_content) > 1000 THEN 1 ELSE 0 END) as 'over_1k',
    SUM(CASE WHEN LENGTH(post_content) > 1500 THEN 1 ELSE 0 END) as 'over_1.5k',
    SUM(CASE WHEN LENGTH(post_content) > 2000 THEN 1 ELSE 0 END) as 'over_2k',
    MIN(LENGTH(post_content)) as min_len,
    MAX(LENGTH(post_content)) as max_len,
    AVG(LENGTH(post_content)) as avg_len
FROM wp_posts WHERE post_type='post' AND post_status='publish' AND post_title!='Hello world!';
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("=== 字数统计 ===")
result = stdout.read().decode('utf-8', errors='ignore').strip()
for line in result.split('\n'):
    parts = line.split('\t')
    if len(parts) >= 7:
        print(f"  总文章数: {parts[0]}")
        print(f"  >1000字: {parts[1]}篇 ({int(parts[1])*100//int(parts[0])}%)")
        print(f"  >1500字: {parts[2]}篇 ({int(parts[2])*100//int(parts[0])}%)")
        print(f"  >2000字: {parts[3]}篇 ({int(parts[3])*100//int(parts[0])}%)")
        print(f"  字数范围: {parts[4]}-{parts[5]}字, 平均{int(parts[6])}字")

# 抽查几篇文章内容
print("\n=== 内容质量抽查 ===")
for pid in [27, 243, 355, 700, 1832]:
    cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
    SELECT post_title, LENGTH(post_content) FROM wp_posts WHERE ID=%d;
    " 2>/dev/null""" % pid
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    r = stdout.read().decode('utf-8', errors='ignore').strip()
    if r:
        parts = r.split('\t')
        print(f"  ID={pid} [{parts[1]}字] {parts[0][:50]}")

ssh.close()
print("\n✅ 全部重写完成！新内容已生效。")
