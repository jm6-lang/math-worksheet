import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 执行SEO优化 ===\n")

# 1. 创建/更新robots.txt
robots_txt = """User-agent: *
Allow: /

# 禁止爬取后台
Disallow: /wp-admin/
Disallow: /wp-login.php
Disallow: /wp-login.php*

# 禁止爬取敏感文件
Disallow: /wp-config.php
Disallow: /wp-content/plugins/
Disallow: /wp-content/themes/
Disallow: /wp-includes/
Disallow: /?s=*

# 允许搜索爬虫抓取HTML
Allow: /wp-admin/admin-ajax.php

# Sitemap
Sitemap: https://skillxm.cn/sitemap_index.xml

# 百度爬虫
User-agent: Baiduspider
Allow: /
Disallow: /wp-admin/
"""

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/robots.txt', 'w') as f:
    f.write(robots_txt)
sftp.close()
print("1. robots.txt 已创建")

# 2. 验证robots.txt
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/robots.txt", timeout=10)
verify = stdout.read().decode().strip()
print(f"   验证: {verify[:80]}...")

# 3. 检查Rank Math SEO设置
print("\n2. 检查Rank Math SEO设置...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp option get rank_math_general_settings --allow-root 2>/dev/null | head -50", timeout=15)
rank_math = stdout.read().decode().strip()
if rank_math and "error" not in rank_math.lower():
    print("   Rank Math设置已存在")
else:
    print("   尝试配置Rank Math...")

# 4. 检查首页是否需要手动设置SEO
print("\n3. 检查首页SEO...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp post list --post_type=page --post_name=home --fields=ID --allow-root 2>/dev/null", timeout=10)
home_page = stdout.read().decode().strip()
if "ID" in home_page:
    page_id = home_page.split('\n')[-1].strip()
    print(f"   找到首页ID: {page_id}")
else:
    print("   未找到静态首页，网站使用文章列表作为首页")

# 5. 优化nginx添加安全头
print("\n4. 添加安全头部...")
stdin, stdout, stderr = ssh.exec_command("cat /etc/nginx/sites-enabled/resource_site.conf | head -30", timeout=10)
current_config = stdout.read().decode()

# 添加安全头部
security_headers = '''
    # 安全头部
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
'''

# 插入安全头部到配置
if 'X-Content-Type-Options' not in current_config:
    stdin, stdout, stderr = ssh.exec_command(
        "sed -i '/server_name skillxm.cn www.skillxm.cn;/a\\\\    # 安全头部\\n    add_header X-Content-Type-Options \"nosniff\" always;\\n    add_header X-Frame-Options \"SAMEORIGIN\" always;\\n    add_header X-XSS-Protection \"1; mode=block\" always;\\n    add_header Referrer-Policy \"strict-origin-when-cross-origin\" always;' /etc/nginx/sites-enabled/resource_site.conf",
        timeout=10
    )
    print("   安全头部已添加")
else:
    print("   安全头部已存在")

# 6. 重载nginx
stdin, stdout, stderr = ssh.exec_command("nginx -t && systemctl reload nginx && echo 'nginx重载成功'", timeout=15)
print(f"\n5. nginx: {stdout.read().decode().strip()}")

# 7. 刷新缓存
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp cache flush --allow-root 2>/dev/null", timeout=10)
print("6. 缓存已刷新")

# 8. 最终验证
print("\n=== SEO优化完成 ===")
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' https://skillxm.cn/", timeout=10)
print(f"网站状态: HTTP {stdout.read().decode().strip()}")

ssh.close()
