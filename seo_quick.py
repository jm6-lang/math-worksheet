import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== SEO检查 ===")

# 1. Sitemap
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' https://skillxm.cn/sitemap_index.xml", timeout=10)
print(f"\n1. Sitemap: {stdout.read().decode().strip()}")

# 2. robots.txt
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/robots.txt", timeout=10)
robots = stdout.read().decode().strip()
print(f"2. robots.txt: {'有' if robots else '无'}")
if robots:
    print(f"   内容: {robots[:150]}...")

# 3. 首页Meta
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/ | grep -oE '<title>[^<]+</title>|<meta name=\"description\" content=\"[^\"]+\"|og:title|canonical' | head -5", timeout=10)
print(f"\n3. 首页Meta:")
print(stdout.read().decode().strip() or "无")

# 4. 结构化数据
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/ | grep -c 'application/ld+json'", timeout=10)
schema_count = stdout.read().decode().strip()
print(f"\n4. Schema结构化数据: {schema_count}个")

# 5. HTTPS重定向
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' http://skillxm.cn/", timeout=10)
print(f"\n5. HTTP->HTTPS: {stdout.read().decode().strip()}")

# 6. 检查SEO插件设置的meta
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp db query \"SELECT meta_key FROM wp_postmeta WHERE meta_key LIKE '%seo%' OR meta_key LIKE '%rank%' LIMIT 10\" --allow-root 2>/dev/null", timeout=15)
print(f"\n6. SEO Meta字段:")
print(stdout.read().decode().strip())

ssh.close()
