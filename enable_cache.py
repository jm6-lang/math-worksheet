import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 启用WP Super Cache插件
commands = [
    "cd /www/wwwroot/resource_site && wp plugin activate wp-super-cache --allow-root 2>&1",
    "cd /www/wwwroot/resource_site && wp super-cache enable --allow-root 2>&1 || echo '可能需要手动配置'",
    "cd /www/wwwroot/resource_site && ls -la wp-content/ | grep cache",
    "cd /www/wwwroot/resource_site && wp option get wp_super_cache_settings --allow-root 2>&1 | head -20"
]

print("=== 启用缓存插件 ===")
for cmd in commands:
    print(f"\n执行: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(f"输出: {output}")
    if error and 'Warning' not in error:
        print(f"错误: {error}")

# 确保缓存目录权限正确
ssh.exec_command("chown -R www-data:www-data /www/wwwroot/resource_site/wp-content/cache 2>/dev/null || mkdir -p /www/wwwroot/resource_site/wp-content/cache && chown www-data:www-data /www/wwwroot/resource_site/wp-content/cache")

ssh.close()
print("\n缓存插件配置完成!")