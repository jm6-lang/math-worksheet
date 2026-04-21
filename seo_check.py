import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== SEO检查 ===\n")

# 1. 检查SEO插件
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp plugin list --status=active --format=table --allow-root 2>/dev/null | grep -i seo", timeout=15)
print("1. SEO插件:")
print(stdout.read().decode().strip() or "未安装SEO插件\n")

# 2. 检查sitemap
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' https://skillxm.cn/sitemap_index.xml", timeout=15)
sitemap_status = stdout.read().decode().strip()
print(f"\n2. Sitemap状态: {sitemap_status}")
if sitemap_status == "200":
    stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/sitemap_index.xml | grep -o '<loc>[^<]*</loc>' | head -5", timeout=15)
    print("   Sitemap内容:", stdout.read().decode().strip()[:200])

# 3. 检查robots.txt
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/robots.txt", timeout=15)
print("\n3. robots.txt:")
print(stdout.read().decode().strip() or "未找到")

# 4. 检查首页meta标签
print("\n4. 首页Meta标签:")
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/ | grep -E '<title>|<meta name=\"description\"|<meta name=\"keywords\"|canonical' | head -10", timeout=15)
meta = stdout.read().decode().strip()
print(meta or "未找到")

# 5. 检查是否有结构化数据
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/ | grep -o 'application/ld+json' | head -1", timeout=15)
has_schema = stdout.read().decode().strip()
print(f"\n5. 结构化数据(Schema): {'有' if has_schema else '无'}")

# 6. 检查HTTPS重定向
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' http://skillxm.cn/", timeout=15)
http_redirect = stdout.read().decode().strip()
print(f"\n6. HTTP->HTTPS重定向: {'正常' if http_redirect == '200' else http_redirect}")

# 7. 检查WWW重定向
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' https://skillxm.cn/ -H 'Host: www.skillxm.cn'", timeout=15)
www_status = stdout.read().decode().strip()
print(f"   www->主域名重定向: {'正常' if www_status == '200' else www_status}")

# 8. 检查图片alt标签（抽样）
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp post list --post_type=post --fields=ID --offset=0 --limit=3 --allow-root", timeout=15)
sample_posts = stdout.read().decode().strip()
print("\n8. 文章SEO检查（抽样）:")
if sample_posts:
    for line in sample_posts.split('\n')[1:]:
        post_id = line.strip()
        if post_id:
            stdin, stdout, stderr = ssh.exec_command(f"cd /www/wwwroot/resource_site && wp post meta get {post_id} _thumbnail_id --allow-root", timeout=10)
            thumb = stdout.read().decode().strip()
            print(f"   文章{post_id}: 缩略图{'有' if thumb else '无'}")

# 9. 检查数据库中SEO meta
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp db query \"SELECT COUNT(*) as total FROM wp_postmeta WHERE meta_key IN ('_yoast_wpseo_title','rank_math_title') AND meta_value != ''\" --allow-root", timeout=15)
seo_count = stdout.read().decode().strip()
print(f"\n9. 已设置SEO Meta的文章:")
print(seo_count)

ssh.close()
