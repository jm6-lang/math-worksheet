import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 网站优化检查 ===\n")

# 1. 检查当前缓存配置
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/wp-config.php | grep -i cache", timeout=10)
print("1. 缓存配置:", stdout.read().decode().strip() or "未配置\n")

# 2. 检查PHP扩展
stdin, stdout, stderr = ssh.exec_command("php -m | grep -i -E 'opcache|redis|memcached|apcu'", timeout=10)
print("2. PHP缓存扩展:", stdout.read().decode().strip() or "无\n")

# 3. 数据库大小
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp db size --format=human --allow-root", timeout=15)
print("3. 数据库大小:", stdout.read().decode().strip() + "\n")

# 4. 内容统计
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp post count --allow-root && wp media count --allow-root", timeout=15)
print("4. 内容统计:")
print(stdout.read().decode().strip() + "\n")

# 5. Nginx Gzip
stdin, stdout, stderr = ssh.exec_command("grep 'gzip' /etc/nginx/sites-enabled/resource_site.conf | head -3", timeout=10)
print("5. Gzip状态:", "已配置" if stdout.read().decode().strip() else "未配置\n")

# 6. PHP OPcache
stdin, stdout, stderr = ssh.exec_command("php -i | grep opcache.enable | head -1", timeout=10)
print("6. OPcache:", stdout.read().decode().strip() + "\n")

# 7. WordPress插件
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp plugin list --status=active --format=table --allow-root 2>/dev/null", timeout=15)
print("7. 活跃插件:")
plugins = stdout.read().decode().strip()
if plugins:
    print(plugins[:500])
else:
    print("   无法获取\n")

ssh.close()
