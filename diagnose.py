import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 诊断采集和SEO问题 ===\n")

# 1. 检查定时任务
print("1. 定时任务状态:")
cmd = "crontab -l 2>/dev/null | grep -v '^#'"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 检查采集日志
print("\n2. 采集脚本日志:")
cmd = "ls -la /www/wwwroot/resource_site/auto_collect/logs/ 2>/dev/null && tail -30 /www/wwwroot/resource_site/auto_collect/logs/cron.log 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode('utf-8', errors='ignore').strip()[-1500:] if stdout.read().decode('utf-8', errors='ignore').strip() else "无日志")

# 3. 检查最新文章
print("\n3. WordPress最新文章:")
cmd = """cd /www/wwwroot/resource_site && wp post list --post_status=publish --orderby=date --order=DESC --posts_per_page=10 --fields=ID,post_title,post_date --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 4. 检查文章总数
print("\n4. 文章总数:")
cmd = """cd /www/wwwroot/resource_site && wp post list --post_status=publish --format=count --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode().strip())

# 5. 检查分类
print("\n5. 文章分类:")
cmd = """cd /www/wwwroot/resource_site && wp term list category --fields=term_id,name,count --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 6. 检查百度验证文件
print("\n6. 百度验证文件:")
cmd = """curl -sI 'https://skillxm.cn/baidu_verify_codeva-YrdJwkcfZ3.html' -k 2>/dev/null | head -5"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 7. 检查robots.txt
print("\n7. robots.txt:")
cmd = """curl -s 'https://skillxm.cn/robots.txt' -k 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# 8. 检查sitemap
print("\n8. Sitemap状态:")
cmd = """curl -sI 'https://skillxm.cn/sitemap_index.xml' -k 2>/dev/null | head -5"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 9. 检查百度站长推送日志
print("\n9. 百度推送记录:")
cmd = "ls -la /www/wwwroot/resource_site/auto_collect/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 10. 检查site是否被百度屏蔽
print("\n10. Nginx配置检查:")
cmd = """grep -i 'baiduspider\|disallow\|User-agent' /www/wwwroot/resource_site/robots.txt 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
