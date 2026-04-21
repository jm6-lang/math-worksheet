import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 确认: Yoast已停用, xenice-seo已激活, footer无sitemap
checks = [
    ("Yoast SEO (inactive)", "wp plugin list --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null | grep wordpress-seo"),
    ("xenice-seo (active)", "wp plugin list --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null | grep xenice"),
    ("wp-super-cache (active)", "wp plugin list --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null | grep super-cache"),
    ("Footer无sitemap", "grep -c 'sitemap_index' /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php"),
    ("主题未变", "wp option get template --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null"),
    ("首页正常", "curl -sk 'https://skillxm.cn/' 2>/dev/null | wc -c"),
]

for label, cmd in checks:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    print(f"  {label}: {out}")

ssh.close()
