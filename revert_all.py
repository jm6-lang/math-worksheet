import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

print("正在撤回所有修改...")

# 1. 停用Yoast，恢复xenice-seo
cmds = [
    # 停用Yoast
    "wp plugin deactivate wordpress-seo --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    # 恢复xenice-seo
    "wp plugin activate xenice-seo --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    # 恢复WP缓存
    "wp plugin activate wp-super-cache --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
]

for c in cmds:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    print(out)

# 2. 恢复wp-config.php原始值
stdin, stdout, stderr = ssh.exec_command("grep -n 'WP_DEBUG\\|WP_CACHE\\|WPCACHEHOME' /www/wwwroot/resource_site/wp-config.php")
print("当前config状态:", stdout.read().decode('utf-8', errors='replace').strip())

# 恢复WPCACHEHOME
ssh.exec_command("sed -i \"s|WPCACHEHOME.*|define( 'WPCACHEHOME', '/www/wwwroot/resource_site/wp-content/plugins/wp-super-cache/' );|\" /www/wwwroot/resource_site/wp-config.php", timeout=10)

# 恢复WP_DEBUG_DISPLAY为false (已经是)
# 不动WP_DEBUG，因为原站也是这样设置的

# 3. 恢复footer.php原始内容 - 先查看当前内容
stdin, stdout, stderr = ssh.exec_command("grep -n 'sitemap_index' /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php")
sitemap_line = stdout.read().decode('utf-8', errors='replace').strip()
print("sitemap行:", sitemap_line)

# 如果有sitemap链接，删除那一行
if sitemap_line:
    line_num = sitemap_line.split(':')[0]
    ssh.exec_command(f"sed -i '{line_num}d' /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php", timeout=10)
    print(f"已删除第{line_num}行的sitemap链接")

# 验证footer已恢复
stdin, stdout, stderr = ssh.exec_command("tail -5 /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php")
print("Footer尾部:", stdout.read().decode('utf-8', errors='replace').strip())

# 4. 恢复文件权限
ssh.exec_command("chown -R www-data:www-data /www/wwwroot/resource_site/", timeout=30)
ssh.exec_command("chmod 755 /www/wwwroot/resource_site/", timeout=10)
print("权限已恢复")

import time
time.sleep(2)

# 5. 测试网站
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=restore' 2>/dev/null | wc -c")
size = stdout.read().decode().strip()
print(f"首页大小: {size} bytes")

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/sitemap_index.xml' 2>/dev/null | head -3")
print("Sitemap:", stdout.read().decode('utf-8', errors='replace').strip())

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=restore' 2>/dev/null | grep -c 'sitemap_index'")
print("Footer无sitemap链接:", stdout.read().decode().strip())

ssh.close()
print("\n已全部恢复。")
