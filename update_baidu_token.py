import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 更新百度推送Token ===\n")

# 1. 查看当前脚本中的百度推送地址
print("1. 当前配置:")
cmd = "grep -n 'BAIDU_PUSH\\|zz.baidu' /www/wwwroot/resource_site/auto_collect/collector.py"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 替换为新的Token
print("\n2. 更新Token...")
cmd = """sed -i 's|http://data.zz.baidu.com/urls?site=skillxm.cn&token=.*|http://data.zz.baidu.com/urls?site=https://www.skillxm.cn\\&token=zJsDaj5ibt8ZlVgz|g' /www/wwwroot/resource_site/auto_collect/collector.py"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)

# 3. 验证
print("\n3. 验证更新:")
cmd = "grep 'BAIDU_PUSH\\|zz.baidu' /www/wwwroot/resource_site/auto_collect/collector.py"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 测试百度推送
print("\n4. 测试百度推送...")
cmd = """echo "https://www.skillxm.cn/" | curl -s --data-binary @- "http://data.zz.baidu.com/urls?site=https://www.skillxm.cn&token=zJsDaj5ibt8ZlVgz" -H "Content-Type:text/plain" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 5. 批量推送已有文章到百度
print("\n5. 批量推送最新文章...")
cmd = """cd /www/wwwroot/resource_site && wp post list --post_status=publish --orderby=date --order=DESC --posts_per_page=20 --fields=url --format=csv --allow-root 2>/dev/null | grep https | tail -10"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
urls = stdout.read().decode().strip()
print("URLs to push:")
print(urls[:500] if urls else "无URL")

if urls:
    # 推送到百度
    url_list = urls.strip().split('\n')
    url_text = '\n'.join(url_list)
    
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/baidu_urls.txt', 'w') as f:
        f.write(url_text)
    sftp.close()
    
    cmd = """curl -s --data-binary @/tmp/baidu_urls.txt "http://data.zz.baidu.com/urls?site=https://www.skillxm.cn&token=zJsDaj5ibt8ZlVgz" -H "Content-Type:text/plain" 2>/dev/null"""
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    result = stdout.read().decode('utf-8', errors='ignore').strip()
    print(f"\n百度推送结果: {result}")

ssh.close()

print("\n✅ 百度推送Token已更新!")
